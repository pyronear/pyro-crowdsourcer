# this target runs checks on all files
quality:
	isort . -c -v
	flake8 ./

# this target runs checks on all files and potentially modifies some of them
style:
	isort .
