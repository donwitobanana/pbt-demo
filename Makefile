
install:
	poetry install -E uvicorn
	pre-commit install

hooks:
	pre-commit run --all-files

run: install
	uvicorn pbt_demo.main:app --reload

test:
	tox .
