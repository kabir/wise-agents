import yaml
from wiseagents.yaml import WiseAgentsLoader


def test_stomp_yaml():
    with open("tests/wiseagents/stomp/test_stomp.yaml") as stream:
        agent = yaml.load(stream, Loader=WiseAgentsLoader)

    assert agent.agent_name == 'Agent1'
    assert agent.host == 'localhost'
    assert agent.port == 61616
