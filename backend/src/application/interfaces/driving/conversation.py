"""
Interface that requires all user interfaces to implement.

User Interfaces like APIs, CLIs, etc should implement this interface,
for consuming conversation use cases.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.conversation import Conversation
from src.domain.message import Message


class ConversationInterface(ABC):
  """Interface for the conversation use case.

  The implementation of this interface should implement the following methods:
  - create_conversation
  - send_message
  - get_conversation_history
  - list_conversations
  - reset_conversation
  """

  @abstractmethod
  def create_conversation(self) -> Conversation:
    """Create a new conversation."""
    pass


  @abstractmethod
  def send_message(self, conversation_id: UUID, message: str) -> None:
    """Send a message to a conversation."""
    pass


  @abstractmethod
  def get_conversation_history(self, conversation_id: UUID) -> list[Message]:
    """Get the conversation history."""
    pass


  @abstractmethod
  def list_conversations(self) -> list[Conversation]:
    """List all conversations."""
    pass


  @abstractmethod
  def reset_conversation(self, conversation_id: UUID) -> None:
    """Reset the conversation history."""
    pass
