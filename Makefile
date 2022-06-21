
install:
	poetry install -E uvicorn
	pre-commit install --hook-type pre-commit --hook-type pre-push

hooks:
	pre-commit run --all-files

run: install
	uvicorn pbt_demo.main:app --reload

test:
	tox .
