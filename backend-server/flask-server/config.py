import os
from flask import Flask
from openai import OpenAI

app = Flask(__name__)

# LMM server URL
LMM_SERVER_URL = "http://localhost:8082/v1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "HISTORY_IMAGE")
LABEL_FOLDER = os.path.join(BASE_DIR, "HISTORY_LABEL")
CROPPED_FOLDER = os.path.join(BASE_DIR, "CROPPED_IMAGES")
DUMMY_DATA_FILE = os.path.join(BASE_DIR, "dummy_data.json")

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(LABEL_FOLDER, exist_ok=True)
os.makedirs(CROPPED_FOLDER, exist_ok=True)

openai_api_key = "EMPTY"
openai_api_base = LMM_SERVER_URL

# Initialize OpenAI client and model
client = OpenAI(api_key=openai_api_key, base_url=openai_api_base)
models = client.models.list()
model = models.data[0].id
