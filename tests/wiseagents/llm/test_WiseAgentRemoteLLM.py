import pytest
import yaml
from wiseagents import WiseAgentRegistry
from wiseagents.llm import OpenaiAPIWiseAgentLLM
from wiseagents.yaml import WiseAgentsLoader


@pytest.fixture(scope="session", autouse=True)
def run_after_all_tests():
    yield
    
    

@pytest.mark.needsllm
def test_openai():
    agent = OpenaiAPIWiseAgentLLM("Answer my greeting saying Hello and my name", "Phi-3-mini-4k-instruct-q4.gguf","http://localhost:8001/v1")
    response = agent.process_single_prompt("Hello my name is Stefano")
    assert "Stefano" in response.content

@pytest.mark.needsllm
def test_openai_with_yaml():
    # If we introduce more tests in this clas, we can get rid of this and use yaml for the new ones
    with open("tests/wiseagents/llm/test_openapi_wise_agent_llm.yaml") as stream:
        agent = yaml.load(stream, Loader=WiseAgentsLoader)

    response = agent.process_single_prompt("Hello my name is Stefano")
    assert "Stefano" in response.content

