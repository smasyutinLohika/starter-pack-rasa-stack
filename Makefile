.PHONY: init clean train-nlu train-core cmdline server check-formatting test

TEST_PATH=./

help:
	@echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    train-nlu"
	@echo "        Trains a new nlu model using the projects Rasa NLU config"
	@echo "    train-core"
	@echo "        Trains a new dialogue model using the story training data"
	@echo "    action-server"
	@echo "        Starts the server for custom action."
	@echo "    cmdline"
	@echo "       This will load the assistant in your terminal for you to chat."


clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf docs/_build
	rm -rf models
	rm -rf tests/models

init:
	pip install pytest==3.5.1
	pip install -r requirements.txt
	pip install rasa_nlu --upgrade
	pip install rasa_core --upgrade
	pip install rasa_core_sdk --upgrade
	python -m spacy download en_core_web_md
	python -m spacy link en_core_web_md en

train-nlu:
	python -m rasa_nlu.train -c nlu_config.yml --data data/nlu_data.md -o models --fixed_model_name nlu --project current --verbose

train-core:
	python -m rasa_core.train -d domain.yml -s data/stories.md -o models/current/dialogue -c policies.yml

cmdline:
	python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml

action-server:
	python -m rasa_core_sdk.endpoint --actions actions

check-formatting:
	pip install black
	black --check .

test:
	python -m pytest tests
