PREFIX ?= $(HOME)/.local

.PHONY: help install uninstall test lint check

help:
	@echo "install     Install appim to $(PREFIX)/bin"
	@echo "uninstall   Remove $(PREFIX)/bin/appim"
	@echo "test        Run the unit tests"
	@echo "lint        Run ruff (pipx install ruff)"
	@echo "check       Run lint + test"

install:
	install -Dm755 appim $(PREFIX)/bin/appim

uninstall:
	rm -f $(PREFIX)/bin/appim

test:
	python3 -m unittest discover -s tests -v

lint:
	ruff check .
	ruff format --check .

check: lint test
