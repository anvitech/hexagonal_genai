"""
Conversation service module that manages the conversations
between the user and the chatbot.

This service is responsible for:
- creating a new conversation,
- sending a message to a conversation,
- listing all conversations,
- getting the conversation history,
- resetting the conversation history.
"""
from uuid import UUID, uuid4

from src.application.interfaces.driving.conversation import ConversationInterface
from src.application.interfaces.driven.llm_provider import LLMProviderInterface
from src.application.interfaces.driven.repository import ConversationRepositoryInterface
from src.domain.conversation import Conversation
from src.domain.message import Message
from src.domain import MessageRole


class ConversationService(ConversationInterface):
  """Chat service.

  This class embeds use cases for generating responses in a conversation
  using a LLM model provider.
  """

  def __init__(self,
               llm_provider: LLMProviderInterface,
               repo: ConversationRepositoryInterface):
    """Initialize the chat service.

    :param LLMProviderInterface llm_provider: LLM model provider.
    :param ConversationRepositoryInterface repo: conversation repository
    """
    self.__llm_provider = llm_provider
    self.__repo = repo


  def create_conversation(self) -> UUID:
    """Create a new conversation.

    New conversation will be created and persisted.

    :return UUID: conversation id
    """
    conversation = self.__repo.get_or_create(id=uuid4())
    return conversation.id


  def send_message(self, conversation_id: UUID, message: str) -> str:
    """Orchestrate the sending of a message in a given conversation.

    :param UUID conversation_id: conversation id.
    :param str message: user message to send.
    :return str: generated response
    :raises ValueError: if conversation_id is not valid
    """
    # Get a conversation
    conversation = self.__repo.get_or_create(id=conversation_id)

    # Add user message
    conversation.add_message(
      Message(id=uuid4(), role=MessageRole.USER, content=message)
    )

    # Generate response
    llm_response = self.__llm_provider.get_response(conversation.messages)

    # Add generated response into history
    conversation.add_message(
      Message(id=uuid4(), role=MessageRole.ASSISTANT, content=llm_response)
    )

    # Persist the conversation
    self.__repo.update(conversation)

    return llm_response


  def get_conversation_history(self, conversation_id: UUID) -> list[Message]:
    """Get the conversation history.

    :param UUID conversation_id: conversation id
    :return list[Message]: conversation history
    :raises ValueError: if conversation_id is not valid
    """
    # Get a conversation given its id
    conversation = self.__repo.get_or_create(id=conversation_id)

    # Return the conversation history
    return conversation.messages


  def list_conversations(self) -> list[Conversation]:
    """List all conversations."""
    return self.__repo.list()


  def reset_conversation(self, conversation_id: UUID) -> None:
    """Reset the conversation history."""
    # Get a conversation given its id
    conversation = self.__repo.get_or_create(id=conversation_id)

    # Reset the conversation
    conversation.messages = []

    # Update the conversation
    self.__repo.update(conversation)

