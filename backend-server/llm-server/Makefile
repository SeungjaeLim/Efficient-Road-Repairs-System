default: build

help:
	@echo 'Management commands for phi-server:'
	@echo
	@echo 'Usage:'
	@echo '    make build            Build the phi3.5 project.'
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
	@docker build . -t phi-server

run:
	@echo "Booting up Docker Container"
	@echo "Running phi-Server"
	@docker run -p 8000:8000 --network phi -it --gpus "device=2" --ipc=host --name phi-server -v `pwd`:/workspace phi-server:latest /bin/bash -c "./run_server.sh"

up: build run

rm: 
	@echo "Removing Docker container"
	@docker rm phi-server

stop:
	@echo "Stopping Docker container"
	@docker stop phi-server

reset: stop rm

docker-setup:
	@echo "Setting up Docker permissions for the current user"
	@sudo groupadd docker || true
	@sudo usermod -aG docker $(USER)
	@newgrp docker

commit:
	@echo "Committing changes to Docker image"
	@docker commit phi-server phi-server:latest
