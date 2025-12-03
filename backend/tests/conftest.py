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


@pytest.fixture(name="llm_cohere_adapter", scope="session")
def llm_cohere_adapter_fixture():
  load_dotenv()
  return LLMCohereAdapter({
    "cohere_api_key": os.environ.get("COHERE_API_KEY"),
    "cohere_model": "command-a-03-2025",
    "cohere_max_messages": 100,
    "system_message": "You are a helpful assistant. You respond in concise sentences.",
  })


@pytest.fixture(name="mocked_messages", scope="session")
def mocked_messages_fixture():
  return [Message(id=uuid4(), role=MessageRole.USER, content="Hello, World!")]
