install:
	pip install -r requirements.txt

run:
	python3 a_maze_ing.py default_config.txt

debug:
	python3 -m pdb a_maze_ing.py default_config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .mypy_cache build dist *.egg-info

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
