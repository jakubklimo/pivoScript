ANTLR=antlr
GRAMMAR=PivoScript.g4
PYTHON=python3
FILEPY=main.py

build:
	$(ANTLR) -Dlanguage=Python3 -visitor $(GRAMMAR)

test-valid: build
	$(PYTHON) $(FILEPY) tests/valid.pivo

test-invalid: build
	$(PYTHON) $(FILEPY) tests/invalid.pivo

clean:
	rm -f PivoScript*.interp
	rm -f PivoScript*.tokens
	rm -f PivoScript*.py