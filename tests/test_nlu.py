from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config


def test_nlu_interpreter():
    training_data = load_data("data/nlu_data.md")
    trainer = Trainer(config.load("nlu_config.yml"))
    interpreter = trainer.train(training_data)

    test_interpreter_dir = trainer.persist("./tests/models")
    assert test_interpreter_dir

    parsing = interpreter.parse("hello")
    assert parsing["intent"]["name"] == "greet"

    parsing = interpreter.parse("I am Rasa")
    assert parsing["intent"]["name"] == "name"
    assert parsing["entities"][0]["value"] == "Rasa".lower()

    parsing = interpreter.parse("bye")
    assert parsing["intent"]["name"] == "goodbye"
