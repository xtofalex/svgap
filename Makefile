.PHONY: doctor test examples verify-artifacts

doctor:
	PYTHONPATH=src python3 -m svgap doctor

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

examples:
	PYTHONPATH=src python3 -m unittest tests.test_examples -v

verify-artifacts:
	PYTHONPATH=src python3 scripts/verify_public_artifacts.py
