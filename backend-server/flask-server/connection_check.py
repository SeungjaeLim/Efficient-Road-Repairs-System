import os
import requests
import base64

# Flask 서버 URL (같은 컴퓨터에서 실행 중인 경우)
SERVER_URL = "http://127.0.0.1:5000/process"

# 현재 디렉터리의 이미지 파일 경로
image_path = os.path.join("./example.jpg")

# 레이블 데이터 (예: YOLO 형식의 바운딩 박스 정보)
labels = "2 100 100 200 200,3 50 50 120 120"

# 이미지 파일을 Base64로 인코딩
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 이미지 Base64 데이터
image_base64 = encode_image_to_base64(image_path)

# POST 요청 데이터 준비
payload = {
    "image": image_base64,
    "labels": labels
}

try:
    # Flask 서버에 POST 요청
    response = requests.post(SERVER_URL, json=payload)

    # 결과 출력
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.status_code, response.text)
except Exception as e:
    print("Exception occurred:", str(e))
