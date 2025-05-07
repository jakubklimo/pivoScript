ANTLR=antlr
GRAMMAR=PivoScript.g4
FILEPY=main.py
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
FILE?=tests/calculator.pivo
OUT_FILE=output/out.txt

run:
	$(PYTHON) $(FILEPY) ${FILE} ${OUT_FILE}

all: install build run

build: clean
	$(ANTLR) -Dlanguage=Python3 -visitor $(GRAMMAR)

install:
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

clean:
	rm -f PivoScript*.interp
	rm -f PivoScript*.tokens
	rm -f PivoScript*.py

help:
	@echo "make build     - Vygeneruje parser z gramatiky"
	@echo "make install   - Vytvoří virtuální prostředí a nainstaluje závislosti"
	@echo "make run       - Spustí skript s výchozím testovacím souborem"
	@echo "make clean     - Odstraní vygenerované soubory"
	@echo "make all       - Provede všechny potřebné kroky"