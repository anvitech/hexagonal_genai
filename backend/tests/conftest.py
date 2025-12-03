import os
from dotenv import load_dotenv
import pytest
from unittest.mock import Mock

from src.infra.llm_adapter import LLMCohereAdapter
from src.domain.message import MessageRole, Message
from uuid import uuid4


@pytest.fixture(name="mocked_llm_provider", scope="session")
def llm_provider_fixture():
  llm_provider = Mock()
  llm_provider.get_response = Mock(return_value="Response from LLM")
  return llm_provider


@pytest.fixture(name="mocked_messages", scope="session")
def mocked_messages_fixture():
  return [Message(id=uuid4(), role=MessageRole.USER, content="Hello, World!")]


@pytest.fixture(name="testing_file_path", scope="session")
def testing_file_path_fixture():
  new_file_path = os.path.join(os.path.dirname(__file__), "test_db.json")
  # Check if the file exists
  if os.path.exists(new_file_path):
    os.remove(new_file_path)
  return os.path.join(os.path.dirname(__file__), "test_db.json")


@pytest.fixture(name="testing_fixed_file_path", scope="session")
def testing_fixed_file_path_fixture():
  return os.path.join(os.path.dirname(__file__), "test_fixed_db.json")


# Connect to Cohere LLM Chat API

@pytest.fixture(name="llm_cohere_adapter", scope="session")
def llm_cohere_adapter_fixture():
  load_dotenv()
  return LLMCohereAdapter({
    "cohere_api_key": os.environ.get("COHERE_API_KEY"),
    "cohere_model": "command-a-03-2025",
    "cohere_max_messages": 100,
    "system_message": "You are a helpful assistant. You respond in concise sentences.",
  })
