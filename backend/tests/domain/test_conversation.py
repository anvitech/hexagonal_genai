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


@pytest.mark.unit
def test_init_from_dict_success():
  data = {
    "id": str(uuid.uuid4()),
    "messages": [
      {
        "id": str(uuid.uuid4()),
        "role": "user",
        "content": "Hello, World!",
        "created_at": datetime.now().isoformat()
      }
    ],
    "created_at": datetime.now().isoformat()
  }

  conversation = Conversation.from_dict(data)

  assert isinstance(conversation.id, uuid.UUID)
  assert len(conversation.messages) == 1
  assert isinstance(conversation.messages[0], Message)


@pytest.mark.unit
@pytest.mark.parametrize("messages", [
  None,
  [],
  [Message(id=uuid.uuid4(), role="user", content="Hello, World!")]
])
def test_conversation_to_dict_success(messages):
  conversation = Conversation(id=uuid.uuid4(), messages=messages)
  assert conversation.to_dict() == {
    "id": str(conversation.id),
    "messages": [m.to_dict() for m in messages] if messages else [],
    "created_at": conversation.created_at.isoformat()
  }
