all: format test

format: format-black format-isort

format-black:
	@echo [black] && poetry run black .

format-isort:
	@echo [isort] && poetry run isort --profile black --filter-files .

test:
	@echo [pytest] && poetry run pytest .

documentation:
    # なぜか動かない
	@poetry run sphinx-apidoc --module-first --separate -f -o ./docs .
	@poetry run sphinx-build -b singlehtml ./docs ./docs/_build
