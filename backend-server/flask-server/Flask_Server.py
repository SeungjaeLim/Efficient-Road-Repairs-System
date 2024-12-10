from flask import Flask, request, jsonify
import base64
import os
import socket
from datetime import datetime
from openai import OpenAI
from Crack_Agent_prompt import crack_agent_prompt

# Flask 앱 초기화
app = Flask(__name__)

# 설정
LMM_SERVER_URL = "http://localhost:8082/v1"  # LMM 서버 URL

# 폴더 생성
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "HISTORY_IMAGE")
LABEL_FOLDER = os.path.join(BASE_DIR, "HISTORY_LABEL")

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(LABEL_FOLDER, exist_ok=True)

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

@app.route('/process', methods=['POST'])
def process_image():
    """
    클라이언트에서 이미지와 라벨 데이터를 받아 처리하고,
    YOLO 결과를 히스토리 폴더에 저장하며, LMM 서버에 전달 하기.
    """
    try:
        print("Request received")
        
        # 요청 데이터 파싱
        data = request.json
        if "image" not in data or "labels" not in data:
            return jsonify({"error": "Missing 'image' or 'labels' field"}), 400

        image_base64 = data["image"]
        labels = data["labels"]

        # 현재 시간으로 고유 파일 이름 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{IMAGE_FOLDER}/image_{timestamp}.jpg"
        label_filename = f"{LABEL_FOLDER}/label_{timestamp}.txt"


        """ 인풋으로 오는 JSON 값
        { 
          "image": "BASE64_ENCODED_IMAGE_DATA",
          "labels": "2 100 100 200 200,3 50 50 120 120"    bounding box는 ,로 구분
        }
        """

        # 이미지를 디코딩하여 파일로 저장
        with open(image_filename, "wb") as img_file:
            img_file.write(base64.b64decode(image_base64))

        # 라벨 데이터를 텍스트 파일로 저장
        with open(label_filename, "w") as lbl_file:
            lbl_file.write(labels)


        #전처리해야할 필요 존재

        #RAG 적용부

        # LMM 서버로 요청 생성
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": crack_agent_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        },
                    },
                ],
            }],
            model=model,
        )

        # 결과 반환
        result = chat_completion.choices[0].message.content


        return jsonify({"message": "Image and labels saved successfully", "lmm_result": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    체크용.
    """
    return jsonify({"status": "running"}), 200


def check_my_ip():
    """
    0.0.0.0 아이피 확인하는 함수
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Google DNS로 연결
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

if __name__ == '__main__':
    real_ip = check_my_ip()
    port = 5000

    print("--------------------------------------------------------")
    print(f"Flask Server is listening on {real_ip}:{port}")
    print("--------------------------------------------------------")

    # Flask 서버 실행
    app.run(host='0.0.0.0', port=port)
