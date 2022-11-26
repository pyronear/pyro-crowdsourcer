# this target runs checks on all files
quality:
	isort . -c
	flake8 ./
	mypy
	black --check .

# this target runs checks on all files and potentially modifies some of them
style:
	isort .
	black .

# Run the docker
run:
	docker-compose up -d --build

# Run the docker
stop:
	docker-compose down
