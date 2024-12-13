from flask import jsonify

def prepare_final_response(lmm_input, original_image_path, boxed_image_path, resized_image_path, output_json_path, final_result, epcis_response):
    """
    Prepare the final JSON response to return to the client.

    :param lmm_input: Input data used for LMM.
    :param original_image_path: Path to the original image.
    :param boxed_image_path: Path to the boxed image.
    :param resized_image_path: Path to the resized image.
    :param output_json_path: Path to the output JSON file.
    :param final_result: The final computed JSON result (including costs).
    :param epcis_response: The response text from the EPCIS server.
    :return: A Flask JSON response tuple.
    """
    return jsonify({
        "message": "Processed successfully and sent to EPCIS server",
        "input": lmm_input,
        "original_image_path": original_image_path,
        "boxed_image_path": boxed_image_path,
        "resized_image_path": resized_image_path,
        "output_json_path": output_json_path,
        "lmm_result": final_result,
        "epcis_response": epcis_response
    }), 200
