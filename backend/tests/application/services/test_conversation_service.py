import pytest
from uuid import uuid4, UUID

from src.application.services.conversation import ConversationService
from src.domain.message import Message
from src.domain.conversation import Conversation
from src.domain import MessageRole


# Unit tests

@pytest.mark.unit
def test_service_create_conversation_success(
    mocked_llm_provider,
    mocked_repository
  ):
  """Service should be able to create a conversation without error."""
  # Init a service object
  conversation_service = ConversationService(
    mocked_llm_provider,
    mocked_repository
  )
  response = conversation_service.create_conversation()
  assert isinstance(response, UUID)


@pytest.mark.unit
def test_conversation_service_send_message_success(
    mocked_llm_provider, mocked_repository
  ):
  """Service should be able to send a message in a conversation without error."""
  conversation_service = ConversationService(
    mocked_llm_provider, mocked_repository
  )
  response = conversation_service.send_message(
    conversation_id=uuid4(),
    message="Hello, World!"
  )
  assert isinstance(response, str)
  assert len(response) > 0


@pytest.mark.unit
def test_service_get_conversation_history_success(
    mocked_llm_provider, mocked_repository
  ):
  """Service should be able to get a conversation history without error."""
  conversation_service = ConversationService(
    mocked_llm_provider, mocked_repository
  )
  response = conversation_service.get_conversation_history(
    conversation_id=uuid4()
  )
  assert isinstance(response, list)
  assert all(
    isinstance(message, Message) for message in response
  )


@pytest.mark.unit
def test_service_list_conversations_success(
    mocked_llm_provider, mocked_repository
  ):
  """Service should be able to list conversations without error."""
  conversation_service = ConversationService(
    mocked_llm_provider, mocked_repository
  )
  response = conversation_service.list_conversations()
  assert isinstance(response, list)
  assert all(
    isinstance(conversation, Conversation) for conversation in response
  )


@pytest.mark.unit
def test_service_reset_conversation_success(
    mocked_llm_provider, mocked_repository
  ):
  """Service should be able to reset a conversation without error."""
  conversation_service = ConversationService(
    mocked_llm_provider, mocked_repository
  )
  conversation_service.reset_conversation(conversation_id=uuid4())


# Integration tests


@pytest.mark.integration
def test_service_create_conversation_with_persistence_success(
    mocked_llm_provider,
    file_repo
  ):
  """Service should be able to create a conversation persisted."""
  conversation_service = ConversationService(
    mocked_llm_provider,
    file_repo
  )
  response = conversation_service.create_conversation()
  assert isinstance(response, UUID)

  # Check if the conversation is persisted
  persisted_conversation = file_repo.get_or_create(id=response)
  assert isinstance(persisted_conversation, Conversation)


@pytest.mark.integration
def test_service_send_message_with_persistence_success(
    mocked_llm_provider,
    file_repo
  ):
  """A new message should be persisted in conversation history."""
  conversation_service = ConversationService(
    mocked_llm_provider,
    file_repo
  )

  # Start a new conversation
  conversation_id = uuid4()

  # Send the first message
  response_1 = conversation_service.send_message(
    conversation_id=conversation_id,
    message="New message 1"
  )
  assert isinstance(response_1, str)
  assert len(response_1) > 0

  # Send the second message
  response_2 = conversation_service.send_message(
    conversation_id=conversation_id,
    message="New message 2"
  )
  assert isinstance(response_2, str)
  assert len(response_2) > 0

  # Check if the conversation is well persisted
  persisted_conversation = file_repo.get_or_create(id=conversation_id)
  assert isinstance(persisted_conversation, Conversation)
  assert persisted_conversation.id == conversation_id
  assert all(
    isinstance(message, Message) for message in persisted_conversation.messages
  )
  assert len(persisted_conversation.messages) == 4

  # Check if the first message is well persisted
  persisted_message_1 = persisted_conversation.messages[0]
  assert isinstance(persisted_message_1, Message)
  assert persisted_message_1.role == MessageRole.USER
  assert persisted_message_1.content == "New message 1"

  # Check if the second message has ASSISTANT role
  persisted_message_2 = persisted_conversation.messages[1]
  assert isinstance(persisted_message_2, Message)
  assert persisted_message_2.role == MessageRole.ASSISTANT
  assert persisted_message_2.content == response_1

  # Check if the third message is well persisted
  persisted_message_3 = persisted_conversation.messages[2]
  assert isinstance(persisted_message_3, Message)
  assert persisted_message_3.role == MessageRole.USER
  assert persisted_message_3.content == "New message 2"

  # Check if the fourth message has ASSISTANT role
  persisted_message_4 = persisted_conversation.messages[3]
  assert isinstance(persisted_message_4, Message)
  assert persisted_message_4.role == MessageRole.ASSISTANT
  assert persisted_message_4.content == response_2
