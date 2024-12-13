from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime
import random
from openai import OpenAI
from Crack_Agent_prompt import crack_agent_prompt
import json
from PIL import Image, ImageDraw
from io import BytesIO
import base64
import requests
from sentence_transformers import SentenceTransformer
import faiss
import logging

# Flask 앱 초기화
app = Flask(__name__)

# 설정
LMM_SERVER_URL = "http://localhost:8082/v1"  # LMM 서버 URL

# 폴더 생성
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "HISTORY_IMAGE")
LABEL_FOLDER = os.path.join(BASE_DIR, "HISTORY_LABEL")
CROPPED_FOLDER = os.path.join(BASE_DIR, "CROPPED_IMAGES")
DUMMY_DATA_FILE = os.path.join(BASE_DIR, "dummy_data.json")

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(LABEL_FOLDER, exist_ok=True)
os.makedirs(CROPPED_FOLDER, exist_ok=True)

# OpenAI 클라이언트 설정
openai_api_key = "EMPTY"
openai_api_base = LMM_SERVER_URL

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# 모델 선택
models = client.models.list()
model = models.data[0].id

# SBERT 및 FAISS 초기화
sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
faiss_index = None
sentences = []

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# ANSI 색상 코드
COLORS = {
    "HEADER": "\033[95m",
    "INFO": "\033[94m",
    "SUCCESS": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "RESET": "\033[0m",
}

def color_text(text, color):
    return f"{COLORS[color]}{text}{COLORS['RESET']}"

def log_request(message):
    logger.info(color_text(f"[Request] {message}", "HEADER"))

def log_retrieval(message):
    logger.info(color_text(f"[Retrieval] {message}", "INFO"))

def log_success(message):
    logger.info(color_text(f"[Success] {message}", "SUCCESS"))

def log_warning(message):
    logger.warning(color_text(f"[Warning] {message}", "WARNING"))

def log_error(message):
    logger.error(color_text(f"[Error] {message}", "ERROR"))

def load_dummy_data():
    global faiss_index, sentences
    try:
        with open(DUMMY_DATA_FILE, "r") as file:
            dummy_data = json.load(file)
        
        # Prepare sentences and embeddings
        sentences = [
            json.dumps(item) for item in dummy_data
            if isinstance(item, dict)
        ]
        unique_sentences = list(set(sentences))
        embeddings = sbert_model.encode(unique_sentences)

        # Create FAISS index
        dimension = embeddings.shape[1]
        faiss_index = faiss.IndexFlatL2(dimension)
        faiss_index.add(embeddings)

        print("Dummy data and FAISS index loaded successfully.")
    except Exception as e:
        print(f"Error loading dummy data: {e}")

def encode_base64_image(image_path):
    """이미지를 Base64 형식으로 인코딩"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_damage_type_label(damage_type_int):
    """Convert integer damage type to string label"""
    damage_type_map = {
        0: "longitudinal crack",
        1: "alligator crack",
        2: "transverse crack",
        3: "other corruption",
        4: "pothole"
    }
    return damage_type_map.get(damage_type_int, "unknown")

def generate_random_geo():
    """Generate random geo coordinates within the defined range."""
    lat = random.uniform(36.361, 36.369)
    lon = random.uniform(127.357, 127.370)
    return f"{lat:.6f},{lon:.6f}"

def retrieve_similar_data(input_data):
    """Retrieve similar data using FAISS and SBERT."""
    try:
        input_sentence = json.dumps(input_data)
        input_embedding = sbert_model.encode([input_sentence])
        D, I = faiss_index.search(input_embedding, k=3)  # Retrieve top 3 matches
        log_retrieval(f"Retrieved indices: {I[0].tolist()}")
        similar_data = [json.loads(sentences[i]) for i in I[0] if i < len(sentences)]
        #print(f"Retrieved Similar Data: {similar_data}")  # Simple debug output
        return similar_data
    except Exception as e:
        #print(f"Error retrieving similar data: {e}")
        return []


@app.route('/static/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    full_path = os.path.join(CROPPED_FOLDER, filename)
    log_request(f"Serving file from: {full_path}")
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
    return send_from_directory(CROPPED_FOLDER, filename)

@app.route('/process', methods=['POST'])
def process_image_and_json():
    try:
        log_request("Request received")
        
        # 이미지와 JSON 데이터 처리
        image_file = request.files.get('image')  # 이미지 파일
        json_data = request.form.get('json')  # JSON 데이터
        
        if not image_file:
            return jsonify({"error": "Missing image file"}), 400
        if not json_data:
            return jsonify({"error": "Missing JSON payload"}), 400
        
        json_data = json.loads(json_data)  # JSON 문자열 파싱
        x1, y1, x2, y2 = json_data.get("x1"), json_data.get("y1"), json_data.get("x2"), json_data.get("y2")
        damage_type_int = json_data.get("label")

        if damage_type_int is None:
            return jsonify({"error": "Missing Damage Type in JSON payload"}), 400

        damage_type = get_damage_type_label(damage_type_int)

        # 이미지 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_image_path = os.path.join(IMAGE_FOLDER, f"original_{timestamp}.png")
        image_file.save(original_image_path)
        
        # 이미지 열기
        with Image.open(original_image_path) as img:
            # Crop 영역 설정 및 저장
            cropped_img = img.crop((x1, y1, x2, y2))
            cropped_image_path = os.path.join(CROPPED_FOLDER, f"cropped_{timestamp}.png")
            cropped_img.save(cropped_image_path)

            # Crop된 이미지를 축소
            cropped_img.thumbnail((256, 256))  # 축소 크기 설정 (256x256)
            resized_image_path = os.path.join(CROPPED_FOLDER, f"resized_{timestamp}.png")
            cropped_img.save(resized_image_path)

            # 축소된 이미지를 Base64로 인코딩
            resized_image_base64 = encode_base64_image(resized_image_path)

            # 빨간 테두리 추가
            draw = ImageDraw.Draw(img)
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            boxed_image_path = os.path.join(CROPPED_FOLDER, f"boxed_{timestamp}.png")
            img.save(boxed_image_path)  # 빨간 테두리 추가된 이미지 저장

        # LMM 서버와 상호작용
        lmm_input = {
            "Damage Type": damage_type,
            "Width": abs(x2 - x1),
            "Height": abs(y2 - y1),
            "CroppedImage": f"data:image/png;base64,{resized_image_base64}"  # 축소된 Base64 이미지
        }

        # Retrieve similar data
        similar_data = retrieve_similar_data(lmm_input)

        #print(f"{crack_agent_prompt}\n\nSimilar Data: {json.dumps(similar_data)}\n\nInput: {json.dumps(lmm_input)}")
        # Chat completion 요청 생성
        chat_input = {
            "role": "user",
            "content": f"{crack_agent_prompt}\n\nSimilar Data: {json.dumps(similar_data)}\n\nInput: {json.dumps(lmm_input)}"
        }

        chat_completion = client.chat.completions.create(
            messages=[chat_input],
            model=model,
        )

        # 결과 처리
        result = chat_completion.choices[0].message.content

        # 불필요한 부분 제거
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.endswith("```"):
            result = result[:-3]

        # JSON 파싱
        try:
            parsed_result = json.loads(result.strip())
        except json.JSONDecodeError as e:
            return jsonify({
                "error": "Failed to parse LMM server response as JSON",
                "details": str(e),
                "raw_result": result
            }), 500

        # `Repair Cost`와 `TotalPrice` 추가
        total_repair_cost = 0
        for item in parsed_result.get("Repair Items", []):
            quantity = item["Quantity"]
            unit_price = item["UnitPrice"]
            total_price = quantity * unit_price
            total_repair_cost += total_price
            item["TotalPrice"] = total_price  # 각 항목에 TotalPrice 추가

        parsed_result["Repair Cost"] = total_repair_cost  # Repair Cost 추가

        # Dimensions는 input에서 가져오기
        parsed_result["Dimensions"] = {
            "Width": lmm_input["Width"],
            "Height": lmm_input["Height"]
        }

        # Damage Type 추가
        parsed_result["Damage Type"] = lmm_input["Damage Type"]

        # 결과를 HISTORY_LABEL에 저장
        output_json_path = os.path.join(LABEL_FOLDER, f"output_{timestamp}.json")
        with open(output_json_path, "w") as output_file:
            json.dump(parsed_result, output_file, indent=4)
        
        # EPCIS 서버로 POST 요청
        epcis_post_data = {
            "@context": [
                "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
                {
                    "https://yourdomain.com/damageType": "https://yourdomain.com/vocab/damageType",
                    "https://yourdomain.com/dimensions": "https://yourdomain.com/vocab/dimensions",
                    "https://yourdomain.com/repairCost": "https://yourdomain.com/vocab/repairCost",
                    "https://yourdomain.com/repairItems": "https://yourdomain.com/vocab/repairItems",
                    "https://yourdomain.com/filename": "https://yourdomain.com/vocab/filename"
                }
            ],
            "type": "ObjectEvent",
            "action": "ADD",
            "bizStep": "repairing",
            "disposition": "in_progress",
            "epcList": ["urn:epc:id:road:0012345"],
            "eventTime": datetime.now().isoformat() + "Z",
            "eventTimeZoneOffset": "+00:00",
            "readPoint": {
                "id": f"urn:epc:id:geo:{generate_random_geo()}"
            },
            "ilmd": {
                "https://yourdomain.com/dimensions": {
                    "Width": lmm_input["Width"],
                    "Height": lmm_input["Height"]
                },
                "https://yourdomain.com/damageType": lmm_input["Damage Type"],
                "https://yourdomain.com/repairCost": {
                    "TotalCost": parsed_result.get("Repair Cost", 0),
                    "items": parsed_result.get("Repair Items", [])
                },
                "https://yourdomain.com/filename": os.path.basename(boxed_image_path)
            }
        }
        headers = {
            "Content-Type": "application/json",
            "GS1-EPCIS-Version": "2.0.0",
            "GS1-CBV-Version": "2.0.0"
        }
        epcis_server_url = "http://192.168.4.7:8090/epcis/v2/events"
        response = requests.post(epcis_server_url, headers=headers, json=epcis_post_data)

        if response.status_code not in [200, 201, 202]:
            return jsonify({
                "error": "Failed to send POST request to EPCIS server",
                "status_code": response.status_code,
                "response_text": response.text
            }), response.status_code

        # 성공적으로 처리된 응답 반환
        return jsonify({
            "message": "Processed successfully and sent to EPCIS server",
            "input": lmm_input,
            "original_image_path": original_image_path,
            "boxed_image_path": boxed_image_path,
            "resized_image_path": resized_image_path,
            "output_json_path": output_json_path,
            "lmm_result": parsed_result,
            "epcis_response": response.text
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    서버 상태 확인용.
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
