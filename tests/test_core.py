import uuid

from actions import ActionJoke
from rasa_core import config
from rasa_core.agent import Agent
from rasa_core.domain import Domain
from rasa_core.policies import KerasPolicy
from rasa_core.trackers import DialogueStateTracker
from rasa_core_sdk.executor import CollectingDispatcher, Tracker


async def test_agent_and_persist():
    policies = config.load("policies.yml")
    policies[0] = KerasPolicy(epochs=2)  # Keep training times low

    agent = Agent("domain.yml", policies=policies)
    training_data = await agent.load_data("data/stories.md")
    agent.train(training_data, validation_split=0.0)
    agent.persist("./tests/models/dialogue")

    loaded = Agent.load("./tests/models/dialogue")

    assert await agent.handle_text("/greet") is not None
    assert loaded.domain.action_names == agent.domain.action_names
    assert loaded.domain.intents == agent.domain.intents
    assert loaded.domain.entities == agent.domain.entities
    assert loaded.domain.templates == agent.domain.templates


def test_action():
    domain = Domain.load("domain.yml")
    dispatcher = CollectingDispatcher()
    uid = str(uuid.uuid1())
    d = DialogueStateTracker(uid, domain.slots).current_state()
    tracker = Tracker.from_dict(d)

    action = ActionJoke()
    action.run(dispatcher, tracker, domain)

    assert "norris" in dispatcher.messages[-1]["text"].lower()
