PYTHON=.venv/bin/python
PIP=.venv/bin/pip

install:
	$(PIP) install -r requirements.txt

run:
	uvicorn app.main:app --reload

format:
	black .
	isort .

lint:
	ruff check .

typecheck:
	mypy app

docker:
	docker compose up --build

docker-down:
	docker compose down

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
