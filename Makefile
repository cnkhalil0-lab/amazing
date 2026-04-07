.PHONY: install run debug clean lint

install:
	pip install --upgrade pip
	pip install flake8 mypy
	pip install setuptools
	pip install build

run:
	python3 a_maze_ing.py config.txt

build:
	python3 -m build

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -f maze.txt

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
