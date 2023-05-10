.PHONY: init clean update lint format


init:
	python3.10 -m venv venv
	(source venv/bin/activate; pip install -r requirements/requirements.txt)

clean:
	rm -rf venv/

update: clean init

lint:
	ruff adventure_llm/

format:
	black adventure_llm/
	isort adventure_llm/

run:
	(source venv/bin/activate; python adventure_llm/main.py)
