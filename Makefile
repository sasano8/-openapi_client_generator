all: format test

format: format-black format-isort

format-black:
	@echo [black] && poetry run black .

format-isort:
	@echo [isort] && poetry run isort --profile black --filter-files .

test:
	@echo [pytest] && poetry run pytest .
