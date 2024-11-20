# Default target
default: build

help:
	@echo 'Management commands for Flask application:'
	@echo
	@echo 'Usage:'
	@echo '    make build            Build the Flask application Docker image.'
	@echo '    make preprocess       Preprocess step (placeholder).'
	@echo '    make run              Run the Flask application Docker container.'
	@echo '    make up               Build and run the Flask application.'
	@echo '    make rm               Remove Docker container.'
	@echo '    make stop             Stop Docker container.'
	@echo '    make reset            Stop and remove Docker container.'
	@echo '    make docker-setup     Setup Docker permissions for the user.'

preprocess:
	@echo "Running preprocess step"
	# Placeholder command for preprocessing
	@echo "Preprocess step completed."

build:
	@echo "Building Docker image"
	docker build . -t flask-app

run:
	@echo "Running Flask Docker container"
	docker run -d --name flask-app -p 5000:5000 flask-app

up: build run

rm:
	@echo "Removing Docker container"
	docker rm -f flask-app || true

stop:
	@echo "Stopping Docker container"
	docker stop flask-app || true

start:
	@echo "Starting Flask Docker container"
	@docker start flask-app || echo "No container found. Please run 'make up' to create and start the container."


reset: stop rm

docker-setup:
	@echo "Setting up Docker permissions for the current user"
	sudo groupadd docker || true
	sudo usermod -aG docker $(USER)
	newgrp docker

commit:
	@echo "Committing changes to Docker image"
	docker commit flask-app flask-app:latest
