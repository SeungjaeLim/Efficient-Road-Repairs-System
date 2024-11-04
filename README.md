# Efficient Road Repairs System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-20.10.7-blue)
![CUDA](https://img.shields.io/badge/CUDA-12.2-green)
![VLLM](https://img.shields.io/badge/VLLM-0.6.3-orange)
![Microsoft Phi](https://img.shields.io/badge/Microsoft-Phi_3.5_vision_instruct-blue)
![PyTorch](https://img.shields.io/badge/Torch-2.4.0-red)
![Transformers](https://img.shields.io/badge/Transformers-4.46.1-purple)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2.0-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.4-teal)


## Overview

The Efficient Road Repairs System is designed to streamline road maintenance by leveraging multimodal inference to assess and prioritize repair tasks. This system uses VLLM, Phi, and other advanced AI and machine learning models to analyze road condition data, optimize repair scheduling, and enhance infrastructure sustainability.

## Project Structure

```text
.
├── client
│   ├── Dockerfile
│   ├── Makefile
│   └── openai_chat_completion_client_for_multimodal.py
└── server
    ├── Dockerfile
    ├── Makefile
    └── run_server.sh
```

## Prerequisites
- **Docker**: Ensure Docker is installed and running.
- **NVIDIA Drivers and CUDA**: Required for GPU support (optional).
- **Python**: Python 3.10 or above (for local testing).

## Setup Instructions

### Step 1: Create Docker Network
To allow communication between client and server containers, create a Docker network:

```bash
docker network create phi
```

### Step 2: Run the Server
1. Navigate to the server directory:
```
cd server
```
2. Build the Docker image, and run the server container, and inside the container, start the VLLM server using Phi:
```
make up
```
This command starts the server on `phi` network and exposes it on port `8000`.

### Step 3: Run the Client
1. Navigate to the client directory:
```
cd client
```

2. Update the client code (Optional) 

(`openai_chat_completion_client_for_multimodal.py`) to point to the server using `phi-server` as the hostname:
```
openai_api_base = "http://phi-server:8000/v1"
```

3. Build the Docker image and run the client container:
```
make up
```


### Step 4: Execute the Client Script
Inside the client container, run the following command to perform a single-image multimodal inference:

```
python openai_chat_completion_client_for_multimodal.py --chat-type single-image
```

This will send a request to the server container running on the Docker network and retrieve inference results.