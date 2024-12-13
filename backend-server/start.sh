#!/bin/bash

echo "Setting up tmux sessions..."

# Create VLLM-Server session
tmux new-session -d -s vllm-server
tmux send-keys -t vllm-server "cd llm-server && ./run_server.sh" C-m

echo "Waiting for VLLM-Server to start..."
sleep 60

# Create Flask-Server session
tmux new-session -d -s flask-server
tmux send-keys -t flask-server "cd flask-server && python app.py" C-m

# Print active tmux sessions
echo "Tmux sessions created:"
tmux list-sessions