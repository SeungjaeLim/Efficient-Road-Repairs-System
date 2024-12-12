#!/bin/bash

echo "Setting up tmux sessions..."

# Create a new tmux session with a split layout for both servers
tmux new-session -d -s server-control -n main

# Split the window vertically (or horizontally if preferred)
tmux split-window -h -t server-control:main

# Start VLLM-Server in the left pane
tmux send-keys -t server-control:0 "cd llm-server && ./run_server.sh" C-m

# Wait 60 seconds before starting Flask-Server
sleep 60

# Start Flask-Server in the right pane
tmux send-keys -t server-control:1 "cd flask-server && python Flask_Server.py" C-m

# Attach to the tmux session with the split view
tmux select-pane -t server-control:0  # Focus on the left pane
tmux attach-session -t server-control
