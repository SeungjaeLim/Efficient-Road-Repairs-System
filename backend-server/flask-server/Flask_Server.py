from flask import Flask, request, jsonify
import os
from datetime import datetime
from openai import OpenAI
from Crack_Agent_prompt import crack_agent_prompt
import json
from PIL import Image
from io import BytesIO
import base64

# Flask 앱 초기화
app = Flask(__name__)

# 설정
LMM_SERVER_URL = "http://localhost:8082/v1"  # LMM 서버 URL

# 폴더 생성
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "HISTORY_IMAGE")
LABEL_FOLDER = os.path.join(BASE_DIR, "HISTORY_LABEL")
CROPPED_FOLDER = os.path.join(BASE_DIR, "CROPPED_IMAGES")

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

def encode_base64_image(image_path):
    """이미지를 Base64 형식으로 인코딩"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

from PIL import Image, ImageDraw

@app.route('/process', methods=['POST'])
def process_image_and_json():
    try:
        print("Request received")
        
        # 이미지와 JSON 데이터 처리
        image_file = request.files.get('image')  # 이미지 파일
        json_data = request.form.get('json')  # JSON 데이터
        
        if not image_file:
            return jsonify({"error": "Missing image file"}), 400
        if not json_data:
            return jsonify({"error": "Missing JSON payload"}), 400
        
        json_data = json.loads(json_data)  # JSON 문자열 파싱
        x1, y1, x2, y2 = json_data.get("x1"), json_data.get("y1"), json_data.get("x2"), json_data.get("y2")
        
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
            "Damage Type": "longitudinal crack",
            "Width": abs(x2 - x1),
            "Height": abs(y2 - y1),
            "CroppedImage": f"data:image/png;base64,{resized_image_base64}"  # 축소된 Base64 이미지
        }
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"{crack_agent_prompt}\n\nInput: {json.dumps(lmm_input)}"
            }],
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

        # 결과를 HISTORY_LABEL에 저장
        output_json_path = os.path.join(LABEL_FOLDER, f"output_{timestamp}.json")
        with open(output_json_path, "w") as output_file:
            json.dump(parsed_result, output_file, indent=4)

        # 성공적으로 처리된 응답 반환
        return jsonify({
            "message": "Processed successfully",
            "input": lmm_input,
            "original_image_path": original_image_path,
            "boxed_image_path": boxed_image_path,
            "resized_image_path": resized_image_path,
            "output_json_path": output_json_path,
            "lmm_result": parsed_result
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
    port = 5000
    print("--------------------------------------------------------")
    print(f"Flask Server is listening on port {port}")
    print("--------------------------------------------------------")
    print(f"Model ID: {model}")
    print("--------------------------------------------------------")
    app.run(host='0.0.0.0', port=port)
