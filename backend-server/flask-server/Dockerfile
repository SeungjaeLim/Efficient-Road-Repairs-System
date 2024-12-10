# Base image for Python and PyTorch
FROM nvcr.io/nvidia/pytorch:23.10-py3

# Upgrade pip and update system
RUN python -m pip install --upgrade pip \
    && apt-get update && apt-get install -y \
    git \
    && apt-get clean

# Set working directory
WORKDIR /workspace

# Copy application files
COPY . /workspace

# Install Python dependencies
RUN pip install flask openai

# Create directories for the Flask server's history folders
RUN mkdir -p /workspace/HISTORY_IMAGE /workspace/HISTORY_LABEL

# Expose the Flask server's port
EXPOSE 5000

# Default command to run the Flask app
CMD ["python", "Flask_Server.py"]
