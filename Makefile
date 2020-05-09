CODE = charamel scripts
TESTS = tests
VENV = poetry run
WIDTH = 88

.PHONY: pretty lint test coverage

pretty:
	$(VENV) black  --skip-string-normalization --line-length $(WIDTH) $(CODE) $(TESTS)
	$(VENV) isort --apply --recursive --line-width $(WIDTH) $(CODE) $(TESTS)
	$(VENV) unify --in-place --recursive $(CODE) $(TESTS)

lint:
	$(VENV) black --check --skip-string-normalization --line-length $(WIDTH) $(CODE) $(TESTS)
	$(VENV) flake8 --statistics --max-line-length $(WIDTH) $(CODE) $(TESTS)
	$(VENV) pylint --rcfile=setup.cfg $(CODE)
	$(VENV) mypy $(CODE)

test:
	$(VENV) pytest -n auto --boxed tests

coverage:
	$(VENV) pytest --cov=charamel
	$(VENV) codecov

benchmark:
	poetry install --extras=benchmark
	$(VENV) python benchmark.py
