#!make
VENV:=.venv
PY_VERSION:=3.12
TARGET:=libzapi
PIP:=$(VENV)/bin/pip
RUFF:=$(VENV)/bin/ruff
UV:=$(VENV)/bin/uv

PRE_COMMIT_LOC:=$(VENV)/.custom_pre_commit_installed

ifeq ($(shell python --version | grep -E $(PY_VERSION) 2> /dev/null),)
	$(error Python $(PY_VERSION) not found)
endif

PRE_COMMIT=$(VENV)/bin/pre-commit
ifneq ($(shell which pre-commit 2> /dev/null),)
	PRE_COMMIT=pre-commit
endif

.PHONY: all
all: build

$(VENV):
	python$(PY_VERSION) -m venv $(VENV)
	$(PIP) install uv

.PHONY: build
build: $(VENV) | $(PRE_COMMIT_LOC)
	$(UV) sync --all-extras

$(PRE_COMMIT_LOC): $(VENV)
	$(PIP) install pre-commit
ifneq ($(shell find . -iname .pre-commit-config.yaml),)
	$(PRE_COMMIT) install
	touch $(PRE_COMMIT_LOC)
endif

.PHONY: clean
clean:
	@rm -r $(VENV)

.PHONY: fmt
fmt: build
	$(RUFF) --config ./pyproject.toml format $(TARGET)

.PHONY: lint
lint: build
	$(RUFF) --config ./pyproject.toml check $(TARGET)
