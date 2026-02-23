"""
Repository interface module.

This module contains:
- ConversationRepositoryInterface: Interface for persisting conversation data.
"""
from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.conversation import Conversation


class ConversationRepositoryInterface(ABC):
  """Repository interface for persisting conversations data."""

  @abstractmethod
  def get_or_create(self, id: UUID) -> Conversation:
    """Get or create a new conversation if it doesn't exist.

    :param UUID id: conversation id
    :return Conversation: conversation
    """
    pass


  @abstractmethod
  def update(self, conversation: Conversation) -> None:
    """Update a conversation.

    :param Conversation conversation: conversation
    """
    pass


  @abstractmethod
  def list(self) -> list[Conversation]:
    """List all conversations.

    :return list[Conversation]: list of conversations
    """
    pass
