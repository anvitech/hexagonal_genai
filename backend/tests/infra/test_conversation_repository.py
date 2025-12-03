import pytest
import uuid
from datetime import datetime

from src.infra.repository import JSONConversationRepository
from src.domain.conversation import Conversation
from src.domain.message import Message


@pytest.mark.unit
def test_get_existing_conversation_success(testing_fixed_file_path):
  repository = JSONConversationRepository(testing_fixed_file_path)
  conversation = repository.get_or_create(
    id=uuid.UUID("2c27746b-bd29-4032-9045-da26f28e79aa")
  )

  assert isinstance(conversation, Conversation)
  assert conversation == Conversation(
    id=uuid.UUID('2c27746b-bd29-4032-9045-da26f28e79aa'),
    messages=[],
    created_at=datetime(2025, 12, 3, 3, 24, 39, 108731)
  )


@pytest.mark.unit
def test_create_new_conversation_success(testing_file_path):
  repository = JSONConversationRepository(testing_file_path)
  conversation = repository.get_or_create(
    id=uuid.uuid4()
  )

  assert isinstance(conversation, Conversation)
  assert len(conversation.messages) == 0


@pytest.mark.unit
def test_list_conversations_success(testing_fixed_file_path):
  repository = JSONConversationRepository(testing_fixed_file_path)
  conversations = repository.list()

  assert isinstance(conversations, list)
  assert len(conversations) == 2

  assert isinstance(conversations[0], Conversation)
  assert isinstance(conversations[1], Conversation)


@pytest.mark.unit
def test_update_conversation_success(testing_fixed_file_path):
  repository = JSONConversationRepository(testing_fixed_file_path)
  conversation = repository.get_or_create(
    id=uuid.UUID("abb3ecb0-aad2-49a2-80de-a8cf583ecf59")
  )

  conversation.add_message(
    Message(id=uuid.uuid4(), role="user", content="Hello, World!")
  )
  conversation.add_message(
    Message(
      id=uuid.uuid4(),
      role="assistant",
      content="The world is beautiful!"
    )
  )

  # Update the conversation
  repository.update(conversation)

  # Reload the conversation for checking
  conversation = repository.get_or_create(
    id=uuid.UUID("abb3ecb0-aad2-49a2-80de-a8cf583ecf59")
  )

  assert isinstance(conversation, Conversation)
  assert len(conversation.messages) == 2
  assert conversation.id == uuid.UUID("abb3ecb0-aad2-49a2-80de-a8cf583ecf59")
