
install:
	poetry install -E uvicorn
	pre-commit install

format:
	pre-commit run --all-files

run: install
	uvicorn pbt_demo.main:app --reload
