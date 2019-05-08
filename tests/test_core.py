from rasa_core import config
from rasa_core.trackers import DialogueStateTracker
from rasa_core.domain import Domain
from rasa_core.agent import Agent
from rasa_core.dispatcher import Dispatcher
from rasa_core.channels import CollectingOutputChannel
from rasa_core.nlg import TemplatedNaturalLanguageGenerator

from actions import ActionJoke
import uuid


def test_agent_and_persist():
    policies = config.load("policies.yml")

    agent = Agent("domain.yml", policies=policies)
    training_data = agent.load_data("data/stories.md")
    agent.train(training_data, validation_split=0.0)

    assert agent.handle_text("/greet")[0]["text"] is not None
    assert agent.handle_text("/goodbye")[0]["text"] is not None
    assert agent.handle_text("/thanks")[0]["text"] is not None

    agent.persist("./tests/models/dialogue")

    loaded = Agent.load("./tests/models/dialogue")

    assert loaded.handle_text("/greet")[0]["text"] is not None
    assert loaded.handle_text("/goodbye")[0]["text"] is not None
    assert loaded.handle_text("/thanks")[0]["text"] is not None

    assert loaded.domain.action_names == agent.domain.action_names
    assert loaded.domain.intents == agent.domain.intents
    assert loaded.domain.entities == agent.domain.entities
    assert loaded.domain.templates == agent.domain.templates


def test_action():
    domain = Domain.load("domain.yml")
    nlg = TemplatedNaturalLanguageGenerator(domain.templates)
    dispatcher = Dispatcher("my-sender", CollectingOutputChannel(), nlg)
    uid = str(uuid.uuid1())
    tracker = DialogueStateTracker(uid, domain.slots)

    action = ActionJoke()
    action.run(dispatcher, tracker, domain)

    assert "norris" in dispatcher.output_channel.latest_output()["text"].lower()
