file_finder = @find . -type f $(1) -not \( -path './venv/*' \)
staged_files = git diff --staged --name-only --diff-filter=d HEAD | grep ${1}

PY_FILES = $(call file_finder,-name "*\.py")
STAGED_PY_FILES = $(call staged_files, -e "\.py")

check: check_format lint

format:
	$(PY_FILES) | xargs black

check_format:
	$(PY_FILES) | xargs black --check

lint:
	$(PY_FILES) | xargs pylint --rcfile=.pylintrc
	$(PY_FILES) | xargs mypy --strict

lint_staged:
	$(STAGED_PY_FILES) | xargs --no-run-if-empty pylint --rcfile=.pylintrc
	$(STAGED_PY_FILES) | xargs --no-run-if-empty mypy --strict --follow-imports=silent

format_staged:
	$(STAGED_PY_FILES) | xargs --no-run-if-empty black --check
