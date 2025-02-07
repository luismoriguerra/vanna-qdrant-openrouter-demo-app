PROJECT_NAME=vannaai-demo-app

# Python environment setup
venv:
	python -m venv venv

install:
	pip install -r requirements.txt

clean:
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Development server
dev:
	gunicorn app.main:app

deploy:
	railway up --service $(PROJECT_NAME) --ci


.PHONY: venv install install-dev clean dev

