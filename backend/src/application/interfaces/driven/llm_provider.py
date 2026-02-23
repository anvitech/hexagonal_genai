"""
LLM provider interface module.

All LLM adapters have to implement this interface.
"""
from abc import ABC, abstractmethod

from src.domain.message import Message


class LLMProviderInterface(ABC):

  @abstractmethod
  def get_response(self, messages: list[Message]) -> str:
    """Generate a response given a list of messages.

    :param list[Message] messages: list of messages.
    :return str: generated response.
    """
    pass


  @abstractmethod
  def get_response_stream(self, messages: list[Message]) -> str:
    """Generate a streamed response given a list of messages.

    :param list[Message] messages: list of messages.
    :return str: generated response.
    """
    raise NotImplementedError
