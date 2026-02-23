"""
LLM Adapter module.

This module contains all adapters implementing the LLMProviderInterface.
"""
from collections import deque
import cohere

from src.application.interfaces.driven.llm_provider import LLMProviderInterface
from src.domain.message import Message
from src.domain import MessageRole


class LLMProviderError(Exception):
  """LLM provider exception related to errors."""
  pass


class LLMProviderConfigError(Exception):
  """LLM provider exception related to configuration."""
  pass


class LLMCohereAdapter(LLMProviderInterface):
  """Cohere LLM adapter."""

  def __init__(self, config: dict) -> None:
    self.__config = config

    # Init the Cohere client object
    if "cohere_api_key" not in self.__config:
      raise LLMProviderError("Cohere API key is not set in .env file!")
    self.__co = cohere.ClientV2(self.__config["cohere_api_key"])


  def get_response(self, messages: list[Message]) -> str:
    """Generate a response given a list of messages.

    :param list[Message] messages: list of messages.
    :return str: generated response.
    """
    try:
      # Add system message into a deque for truncation purposes
      final_messages = self.__add_system_message(messages)

      # Generate response
      response = self.__co.chat(
        model=self.__config["cohere_model"],
        messages=final_messages,
      )

      return response.message.content[0].text
    except KeyError as e:
      raise LLMProviderConfigError(f"Error on Cohere config object: {e}")
    except cohere.BadRequestError as e:
      raise LLMProviderConfigError(f"Failed to generate response, LLM provider error: {e}")
    except Exception as e:
      raise LLMProviderError(f"Failed to generate response, unhandled error: {e}")


  def get_response_stream(self, messages: list[Message]) -> str:
    raise NotImplementedError


  # privates


  def __add_system_message(self, messages: list[Message]) -> list[dict]:
    """Add a predefined system message into a given list of messages.

    :param list[Message] messages: list of messages.
    :return list[dict]: truncated list of messages.
    """
    # Add system message into a deque for truncation purposes
    _messages = deque(maxlen=self.__config.get("cohere_max_messages", None))
    _messages.extend(map(LLMCohereAdapter.__message_converter, messages))
    _messages.appendleft(
      {
        'role': MessageRole.SYSTEM.value,
        'content': self.__config["system_message"]
      }
    )
    return list(_messages)


  @staticmethod
  def __message_converter(message: Message) -> dict:
    """Convert a message to a dictionary.

    :param Message message: message to convert.
    :return dict: dictionary representation of the message.
    """
    return {"role": message.role.value, "content": message.content}
