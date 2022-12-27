
get going: build run

build:
	pipenv run python3 -m build

run:
	flask run --reload

test_db:
	pytest tests/test_db.py

test_api:
	python3 -m pytest tests/test_auth.py
	python3 -m pytest test/test_insults.py

test_utils:
	pytest tests/test_utils.py