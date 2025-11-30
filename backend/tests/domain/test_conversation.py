from datetime import datetime
import pytest

from src.domain.conversation import Conversation
from src.domain.message import Message
import uuid

@pytest.mark.unit
def test_conversation_init_success():
  conversation = Conversation(id=uuid.uuid4())

  assert isinstance(conversation.id, uuid.UUID)
  assert isinstance(conversation.messages, list)
  assert isinstance(conversation.created_at, datetime)
  assert len(conversation.messages) == 0

  conversation.add_message(
    Message(
      id=uuid.uuid4(), role="user", content="Hello, World!"
    )
  )
  assert len(conversation.messages) == 1
