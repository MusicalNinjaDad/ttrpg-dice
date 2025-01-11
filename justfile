venv := ".venv"

# list available recipes
list:
  @just --list --justfile {{justfile()}}
  
# remove pre-built python libraries (excluding those in .venvs)
clean:
    rm -rf .pytest_cache
    rm -rf build
    rm -rf test/assets/build
    rm -rf dist
    rm -rf wheelhouse
    rm -rf .ruff_cache
    find . -depth -type d -not -path "./.venv*/*" -name "__pycache__" -exec rm -rf "{}" \;
    find . -depth -type d -path "*.egg-info" -exec rm -rf "{}" \;
    find . -type f -name "*.egg" -delete
    find . -type f -name "*.so" -delete

# clean out coverage files
clean-cov:
    rm -rf pycov

# clean, remove existing .venvs and rebuild the venvs with pip install -e .[dev]
reset: clean clean-cov && install (install "python3.12" ".venv-3.12" "[lint,test]")
    rm -rf .venv*

# (re-)create a venv and install the project and required dependecies for development & testing
install python="python" venvpath=venv extras="[dev]":
    rm -rf {{venvpath}}
    {{python}} -m venv {{venvpath}}
    {{venvpath}}/bin/python -m pip install --upgrade pip 
    {{venvpath}}/bin/pip install -e .{{extras}}

# lint python with ruff
lint:
  {{venv}}/bin/ruff check .

# test python
test:
  {{venv}}/bin/pytest

# type-check python
type-check venvpath=".venv-3.12":
  {{venvpath}}/bin/pytype .

# lint and test python
check:
  @- just lint
  @- just test
  @- just type-check

#run coverage analysis on python code
cov:
  {{venv}}/bin/pytest --cov --cov-report html:pycov --cov-report term

# serve python coverage results on localhost:8000 (doesn't run coverage analysis)
show-cov:
  python -m http.server -d ./pycov

# serve python docs on localhost:8000
docs:
  mkdocs serve