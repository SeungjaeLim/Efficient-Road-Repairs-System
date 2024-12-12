#!/bin/bash

echo "Stopping tmux sessions..."

# Kill the tmux sessions for vllm-server and flask-server
tmux kill-session -t vllm-server 2>/dev/null
tmux kill-session -t flask-server 2>/dev/null

echo "Tmux sessions stopped."
