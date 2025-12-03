"""Conversation domain entity."""

from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from src.domain.message import Message


@dataclass
class Conversation:
  """Conversation class.

  This class handles the conversation between the user and the chatbot.
  """

  id: UUID
  messages: list[Message] | None = None
  created_at: datetime = datetime.now()


  def __post_init__(self):
    """Initialize the conversation messages with an empty list.

    This is useful in case of no given messages
    """
    if self.messages is None:
      self.messages = []


  def add_message(self, message: Message) -> None:
    """Add a message to the conversation."""
    self.messages.append(message)
