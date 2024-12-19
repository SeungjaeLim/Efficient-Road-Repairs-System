![{012E35F3-F81B-41FD-92F1-7C0D4B68187F}](https://github.com/user-attachments/assets/3de63702-14e7-4cbb-a5d3-5ae34de97da3)




![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-20.10.7-blue)
![Flask](https://img.shields.io/badge/Flask-2.2.2-green)
![FAISS](https://img.shields.io/badge/FAISS-1.7.0-purple)
![React](https://img.shields.io/badge/React-18.0.0-blue)
![VLLM](https://img.shields.io/badge/VLLM-0.6.4-orange)
![SBERT](https://img.shields.io/badge/SBERT-bert--base--nli--mean--tokens-teal)
![Model](https://img.shields.io/badge/LMM-Microsoft%2FPhi--3.5--vision--instruct-blue)

---

<p align="center">
  <a href="https://github.com/JJong84/ALLeX">
  </a>
    <a href="https://github.com/SeungjaeLim/Efficient-Road-Repairs-System/blob/main/Final%20Project.pdf">Presentation</a>
    <a>&emsp;&emsp;</a>
    <a href="https://github.com/SeungjaeLim/Efficient-Road-Repairs-System/blob/main/Demo.mp4">Demo Video</a>
  </p>
  


</p>
![{A2C834C0-711F-4A9C-9916-E827ECB52532}](https://github.com/user-attachments/assets/dae2d157-4d90-4ccf-a951-39a15e33ac27)

## Overview

The **Efficient Road Repairs System** utilizes **FPGA-porting** of **YOLO** to detect road damage through vehicle black boxes during driving. The system employs a Large **Multi-modal Model (LMM) RAG** to generate repair cost estimates and stores this information in a **GS1 EPCIS** server, enabling centralized governmental management by web.

## Features

- **YOLOv8 Damage Detection**: Trained on the RDD2022 dataset.
- **FPGA Porting**: Optimized for in-vehicle black box systems.
- **VLLM Serve**: Efficient, high-throughput inference for LLMs.
- **Multimodal Inference**: Utilizing Phi 3.5 for damage analysis and cost estimation.
- **Retrieval-Augmented Generation (RAG)**: Powered by FAISS for efficient data retrieval.
- **EPCIS Integration**: Manages repair event tracking via GS1-compliant server.
- **Government Dashboard**: React-based web interface for road damage management.

## Project Structure

```text
rrsys
├── backend
│   ├── flask-server       # Flask-based backend server
│   ├── llm-server         # VLLM inference engine
├── dashboard              # React web application
└── epcis-application-2.0  # GS1-compliant EPCIS server
```

## Setup Instructions

### Backend Setup

1. Start the backend services:

   ```bash
   ./run/start_backend.sh
   ```

2. Inside the Docker container, execute:

   ```bash
   ./start.sh
   ```

3. To stop the backend services:

   ```bash
   ./stop.sh
   ```
   The backend server will be available at `http://localhost:5000`.
   
   The vllm server will be available at `http://localhost:8082`.

### EPCIS Server Setup

1. Start the EPCIS server:

   ```bash
   ./run/start_gs1.sh
   ```

2. To initialize the EPCIS Swagger UI:

   ```bash
   cd epcis-application-2.0/src
   npm install
   node openApi.js
   ```

   The EPCIS server will be available at `http://localhost:8090`.

   The EPCIS swagger will be available at `http://localhost:8081`.

### Web Dashboard Setup

1. Start the web dashboard:

   ```bash
   ./run/start_web
   ```
    The dashboard web will be available at `http://localhost:3000`.

## Usage

### 1. Detecting Road Damage

- Road damage images and YOLO outputs are processed through the FPGA-integrated black box.
- Detected damage types include longitudinal cracks, alligator cracks, transverse cracks, other corruptions, and potholes.

![image](https://github.com/user-attachments/assets/c2f6bc82-19e5-4fc8-ac4e-b557197914e0)

![{FFAE9EF6-B7AB-42C9-B2DE-32A8C915AC7A}](https://github.com/user-attachments/assets/7ff5db13-50a9-4c03-a322-594b690cf3b4)

![{B51F03A2-A88F-46C6-B0F4-194315FE4653}](https://github.com/user-attachments/assets/c5c4c18a-16c1-4fd8-b920-fdceaca61026)


### 2. Generating Repair Estimates

- The system uses Phi 3.5 and RAG to generate detailed repair cost estimates based on the detected damage.

![{E19B7A2E-D01E-424A-BC66-16235BB40EFE}](https://github.com/user-attachments/assets/136eec91-df55-4332-b448-31e8ca8f7ea3)
![{8F82693C-4BBD-4EC5-9077-62B945BD8B1B}](https://github.com/user-attachments/assets/2061d018-d073-4522-b058-c00c2cbdbc0c)


![{1954376C-2DBD-4AC3-8BA6-3466DBB92DF7}](https://github.com/user-attachments/assets/18f57ed8-d608-4ecd-9ea8-c530f5b93815)
![{FD84B347-A998-4D72-906E-FDA0929A1538}](https://github.com/user-attachments/assets/968bb364-706b-4c6b-98aa-bfd77ff4d377)
![{EB9C144D-CDC7-4EEC-AAA1-2DEC5D211BC8}](https://github.com/user-attachments/assets/80a4bd77-8605-4644-b4e0-edf58da9cfcf)

### 3. Managing Events via EPCIS

- The repair cost estimates, along with metadata such as damage dimensions and geolocation, are stored in the GS1 EPCIS server for centralized tracking.

![{453E2109-C957-4DD8-AD5C-5D0B6B742D8D}](https://github.com/user-attachments/assets/87bb71e3-941d-4f5f-bb1a-cd210994ae91)

![{ED3E0F31-9F85-4BC7-B61F-42023FB7BBB3}](https://github.com/user-attachments/assets/987a1a8b-2b3d-4475-ad48-47d44e0d986d)
![{9CBC9C68-8554-42CF-B88B-3CDDF1F1896C}](https://github.com/user-attachments/assets/0b0301f5-1897-45e1-8845-2c1c2729c5b9)

### 4. Viewing and Managing Events

- Use the React dashboard to visualize and manage damage reports:
  - View repair costs, damage types, and geolocations.
  - Monitor historical repair events.

![image](https://github.com/user-attachments/assets/f73a7d62-cfc6-4679-9905-f7711727fcb4)
![image](https://github.com/user-attachments/assets/355dc65b-ed7e-465e-b6ea-e1b7d5b2fe0b)

### EPCIS Integration

- Events can be queried and managed via the EPCIS API:
  - **Swagger UI**: `http://localhost:8081`.
  - **API Endpoints**: Supports event queries, capture, and subscriptions.

## Technologies Used

- **YOLOv8**: For road damage detection.
- **FPGA**: Optimized inference for in-vehicle systems.
- **Flask**: Backend API.
- **React**: Frontend framework.
- **FAISS**: Efficient similarity search for RAG.
- **VLLM Serve**: Fast Multimodal inference.
- **EPCIS**: Event tracking and integration.

## Contributions

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
