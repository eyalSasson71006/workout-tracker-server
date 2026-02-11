VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Run the application
run:
	$(PYTHON) main.py

# Install dependencies from requirements.txt
install:
	$(PIP) install -r requirements.txt

# Add a new dependency: usage -> make add dep=flask
add:
	$(PIP) install $(dep)
	$(PIP) freeze > requirements.txt

# Create the virtual environment
venv:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Remove the virtual environment
clean:
	rm -rf $(VENV)

.PHONY: run install add clean
