.PHONY: install test validate demo clean

install:
	python3 -m pip install -e .

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

validate:
	PYTHONPATH=src python3 -m sequence_design validate

demo:
	PYTHONPATH=src python3 examples/verify_zcp.py

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf build dist *.egg-info src/*.egg-info

