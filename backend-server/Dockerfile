# Base image for Python and PyTorch
FROM nvcr.io/nvidia/pytorch:23.10-py3

# Upgrade pip and update the system
RUN python -m pip install --upgrade pip \
    && apt-get update && apt-get install -y \
    git tmux \
    && apt-get clean

# Set up working directory
RUN mkdir -p /workspace
WORKDIR /workspace

# Copy application files to the workspace
COPY . /workspace

# Install Python dependencies
RUN pip install --default-timeout=1000000 --no-cache-dir \
    flask \
    openai \
    vllm \
    faiss-gpu \
    Pillow \
    sentence-transformers \
    requests

# Create directories for the Flask server's history folders
RUN mkdir -p /workspace/client/HISTORY_IMAGE /workspace/client/HISTORY_LABEL

# Expose ports for Flask and other services
EXPOSE 5000
EXPOSE 8082

# Default command: Start an interactive shell
CMD ["bash"]
