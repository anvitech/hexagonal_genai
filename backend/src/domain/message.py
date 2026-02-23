"""
Message domain entity.
"""
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from src.domain import MessageRole


@dataclass
class Message:
  """Represents a message that a user can send to the chatbot."""

  id: UUID
  role: MessageRole
  content: str
  created_at: datetime = datetime.now()


  @classmethod
  def from_dict(cls, data: dict) -> None:
    """Create a conversation from a dictionary."""
    return cls(**{
      **data,
      "id": UUID(data["id"]),
      "role": MessageRole(data["role"]),
      "created_at": datetime.fromisoformat(data["created_at"]),
    })


  def __post_init__(self):
    """Validate the message attributes."""
    # Validate the id
    if not isinstance(self.id, UUID):
      raise ValueError(f"Invalid id: {self.id}")

    # Validate the role
    if isinstance(self.role, str):
      self.role = MessageRole(self.role.lower())

    # Validate the content
    if not isinstance(self.content, str):
      raise ValueError(f"Invalid content: {self.content}")


  def to_dict(self):
    """Convert the message to a dictionary."""
    return {
      "id": str(self.id),
      "role": self.role.value,
      "content": self.content,
      "created_at": self.created_at.isoformat()
    }
