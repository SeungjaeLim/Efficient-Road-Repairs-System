#!/bin/bash

echo "Setting up tmux sessions..."

# Create VLLM-Server session
tmux new-session -d -s vllm-server
tmux send-keys -t vllm-server "cd server && ./run_server.sh" C-m

# Create Flask-Server session
tmux new-session -d -s flask-server
tmux send-keys -t flask-server "cd client && python Flask_Server.py" C-m

# Print active tmux sessions
echo "Tmux sessions created:"
tmux list-sessions
