# Default target
default: build

help:
	@echo 'Management commands for rrsys-server:'
	@echo
	@echo 'Usage:'
	@echo '    make build            Build the rrsys project.'
	@echo '    make preprocess       Preprocess step.'
	@echo '    make run              Boot up Docker container.'
	@echo '    make up               Build and run the project.'
	@echo '    make rm               Remove Docker container.'
	@echo '    make stop             Stop Docker container.'
	@echo '    make reset            Stop and remove Docker container.'
	@echo '    make docker-setup     Setup Docker permissions for the user.'
	@echo '    make commit           Commit changes to the Docker image.'

preprocess:
	@echo "Running preprocess step"
	# Add preprocessing steps if needed

build:
	@echo "Building Docker image"
	@docker build . -t rrsys

run:
	@echo "Booting up Docker Container"
	@echo "Running rrsys-server"
	@docker run -p 5000:5000 -p 8082:8082 \
		-it --gpus "device=0" --ipc=host \
		--name rrsys-server -v `pwd`:/workspace rrsys:latest /bin/bash

up: build run

rm:
	@echo "Removing Docker container"
	@docker rm rrsys-server

stop:
	@echo "Stopping Docker container"
	@docker stop rrsys-server

reset: stop rm

docker-setup:
	@echo "Setting up Docker permissions for the current user"
	@sudo groupadd docker || true
	@sudo usermod -aG docker $(USER)
	@newgrp docker

commit:
	@echo "Committing changes to Docker image"
	@docker commit rrsys-server rrsys:latest
