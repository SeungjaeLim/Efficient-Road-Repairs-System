from flask import request, jsonify, send_from_directory
import os
import json

from config import app, CROPPED_FOLDER, IMAGE_FOLDER, LABEL_FOLDER, model
from utils import log_request, log_error
from retrieval import load_dummy_data
from services.image_service import (save_original_image, process_image, generate_timestamp)
from services.lmm_service import get_lmm_result
from services.cost_service import calculate_total_costs
from services.response_service import prepare_final_response
from services.epcis_service import send_to_epcis
from prompt import crack_agent_prompt


@app.route('/static/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    """
    Serve images from the CROPPED_IMAGES directory.

    :param filename: The name of the image file to serve.
    :return: The requested file or a 404 if not found.
    """
    full_path = os.path.join(CROPPED_FOLDER, filename)
    log_request(f"Serving file from: {full_path}")
    if not os.path.exists(full_path):
        log_error(f"File not found: {full_path}")
    return send_from_directory(CROPPED_FOLDER, filename)


@app.route('/process', methods=['POST'])
def process_image_and_json():
    """
    Handle the image processing and data enrichment logic:
    1. Validate and parse the input (image and JSON).
    2. Process the image (crop, resize, box drawing).
    3. Interact with LMM (OpenAI) service to get repair suggestions.
    4. Calculate costs and finalize the output JSON.
    5. Send event data to EPCIS server.
    6. Return the final JSON response.

    :return: A JSON response with final results.
    """
    try:
        log_request("Request received")

        image_file = request.files.get('image')
        json_data_str = request.form.get('json')

        # Validate input
        if not image_file:
            return jsonify({"error": "Missing image file"}), 400
        if not json_data_str:
            return jsonify({"error": "Missing JSON payload"}), 400

        json_data = json.loads(json_data_str)
        x1, y1 = json_data.get("x1"), json_data.get("y1")
        x2, y2 = json_data.get("x2"), json_data.get("y2")
        damage_type_int = json_data.get("label")

        if damage_type_int is None:
            return jsonify({"error": "Missing Damage Type in JSON payload"}), 400

        # Generate timestamp and paths
        timestamp = generate_timestamp()
        original_image_path = save_original_image(image_file, IMAGE_FOLDER, timestamp)

        # Process the image and prepare LMM input
        image_paths, lmm_input = process_image(
            original_image_path, x1, y1, x2, y2, damage_type_int, timestamp
        )

        # Interact with LMM server
        lmm_result = get_lmm_result(lmm_input, crack_agent_prompt, model)

        # Calculate total costs and finalize JSON output
        final_result = calculate_total_costs(lmm_result, lmm_input)
        output_json_path = os.path.join(LABEL_FOLDER, f"output_{timestamp}.json")
        with open(output_json_path, "w") as output_file:
            json.dump(final_result, output_file, indent=4)

        # Send event to EPCIS server
        epcis_response = send_to_epcis(final_result, lmm_input, image_paths["boxed"])

        # Return final response
        return prepare_final_response(
            lmm_input,
            original_image_path,
            image_paths["boxed"],
            image_paths["resized"],
            output_json_path,
            final_result,
            epcis_response
        )

    except Exception as e:
        log_error(str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the server is running.

    :return: JSON response indicating server status.
    """
    return jsonify({"status": "running"}), 200


if __name__ == '__main__':
    load_dummy_data()
    port = 5000
    print("--------------------------------------------------------")
    print(f"Flask Server is listening on port {port}")
    print("--------------------------------------------------------")
    print(f"Model ID: {model}")
    print("--------------------------------------------------------")
    app.run(host='0.0.0.0', port=port)
