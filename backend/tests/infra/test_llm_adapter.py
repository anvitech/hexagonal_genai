import pytest

from src.infra.llm_adapter import LLMCohereAdapter, LLMProviderError


@pytest.mark.unit
def test_init_has_exception():
  with pytest.raises(LLMProviderError):
    LLMCohereAdapter({})


@pytest.mark.integration
def test_get_response_success(llm_cohere_adapter, mocked_messages):
  response = llm_cohere_adapter.get_response(mocked_messages)
  assert isinstance(response, str)
  assert len(response)>0