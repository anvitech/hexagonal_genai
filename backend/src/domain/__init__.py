"""Domain layer package.

That contains the core business logic and domain entities of the application.
"""
from enum import Enum

class MessageRole(Enum):
  """Message role type definition."""

  USER = "user"
  ASSISTANT = "assistant"
  SYSTEM = "system"
