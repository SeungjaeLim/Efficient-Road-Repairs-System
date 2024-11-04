FROM nvcr.io/nvidia/pytorch:23.10-py3

# Upgrade pip
RUN python -m pip install --upgrade pip

# Update and install git
RUN apt-get update && apt-get install git -y

# Create a workspace directory and set it as the working directory
RUN mkdir -p /workspace 
WORKDIR /workspace 

# Install vllm and configure pip with retry and timeout options to avoid installation timeouts

# Expose port 8000
EXPOSE 8000:8000

RUN pip install vllm

# Test PyTorch installation and CUDA availability
RUN python -c "import torch; print(torch.__version__)"
RUN python -c "import torch; print(torch.cuda.is_available())"
