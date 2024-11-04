default: build

help:
	@echo 'Management commands for phi-client:'
	@echo
	@echo 'Usage:'
	@echo '    make build            Build the phi-client project.'
	@echo '    make preprocess       Preprocess step.'
	@echo '    make run              Boot up Docker container.'
	@echo '    make up               Build and run the project.'
	@echo '    make rm               Remove Docker container.'
	@echo '    make stop             Stop Docker container.'
	@echo '    make reset            Stop and remove Docker container.'
	@echo '    make docker-setup     Setup Docker permissions for the user.'

preprocess:
	@echo "Running preprocess step"
	@docker 

build:
	@echo "Building Docker image"
	@docker build . -t phi-client
run:
	@echo "Booting up Docker Container"
	@docker run -it --gpus "device=3" --ipc=host --network phi --name phi-client -v `pwd`:/workspace phi-client:latest /bin/bash

up: build run

rm: 
	@echo "Removing Docker container"
	@docker rm phi-client

stop:
	@echo "Stopping Docker container"
	@docker stop phi-client

reset: stop rm

docker-setup:
	@echo "Setting up Docker permissions for the current user"
	@sudo groupadd docker || true
	@sudo usermod -aG docker $(USER)
	@newgrp docker

commit:
	@echo "Committing changes to Docker image"
	@docker commit phi-client phi-client:latest
