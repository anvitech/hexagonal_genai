import pytest
import uuid
from datetime import datetime
from dataclasses import asdict

from src.domain.message import Message
from src.domain import MessageRole

@pytest.mark.unit
def test_message_init_success():
  msg = Message(
    id=uuid.uuid4(),
    role=MessageRole.USER,
    content="Hello, World!"
  )

  assert isinstance(msg.id, uuid.UUID)
  assert msg.content == "Hello, World!"
  assert msg.role == MessageRole.USER
  assert isinstance(msg.created_at, datetime)


@pytest.mark.unit
@pytest.mark.parametrize(
  "id, role, content, error", [
  (None, "user", "Hello, World!", "Invalid id: None"),
  (uuid.uuid4(), "role", "Hello, World!", "Invalid role: role"),
  (uuid.uuid4(), "user", None, "Invalid content: None"),
])
def test_message_init_with_error(id, role, content, error):
  with pytest.raises(ValueError, match=error):
    Message(id=id, role=role, content=content)


@pytest.mark.unit
def test_message_to_dict_success():
  msg = Message(
    id=uuid.uuid4(),
    role=MessageRole.USER,
    content="Hello, World!"
  )

  assert msg.to_dict() == {
    'id': str(msg.id),
    'role': 'user',
    'content': 'Hello, World!',
    'created_at': msg.created_at.isoformat()
  }
