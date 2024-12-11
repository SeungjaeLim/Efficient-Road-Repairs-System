import os
import requests
import json

# Flask 서버 URL
SERVER_URL = "http://127.0.0.1:5000/process"

# JSON 파일 경로
data_json_path = "./data/data.json"
images_dir = "./data/images"

# JSON 데이터 읽기
def read_json(json_path):
    with open(json_path, "r") as file:
        return json.load(file)

def send_data_to_server(json_data, images_dir):
    for entry in json_data:
        filename = entry.get("filename")
        if not filename:
            print("Error: Missing 'filename' in JSON entry.")
            continue
        
        image_path = os.path.join(images_dir, filename)
        if not os.path.exists(image_path):
            print(f"Error: Image file not found: {image_path}")
            continue
        
        try:
            # JSON 데이터를 확인하기 위해 출력
            print("Sending JSON data:", json.dumps(entry, indent=4))

            # 이미지와 JSON 데이터를 multipart/form-data로 전송
            with open(image_path, "rb") as image_file:
                files = {"image": image_file}
                data = {"json": json.dumps(entry)}  # JSON 데이터를 문자열로 전달
                
                # 서버로 POST 요청
                response = requests.post(SERVER_URL, files=files, data=data)
                
                if response.status_code == 200:
                    print(f"Success for {filename}: {response.json()}")
                else:
                    print(f"Error for {filename}: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Exception occurred for {filename}: {str(e)}")

# 실행
if __name__ == "__main__":
    # JSON 데이터 읽기
    json_data = read_json(data_json_path)

    # 서버로 전송
    send_data_to_server(json_data, images_dir)
