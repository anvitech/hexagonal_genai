"""
Repository module for persisting conversations data.

Each repository in this module has to implement the corresponding interface
defined in the `application.interfaces.driven.repository` module.
"""
from uuid import UUID
import json

from src.application.interfaces.driven.repository import ConversationRepositoryInterface
from src.domain.conversation import Conversation


class ConversationNotFoundError(Exception):
  """Exception raised when a conversation is not found."""
  pass


#######################
# JSON Repository
#######################

class ConversationJSONPersistenceError(Exception):
  """Exception raised when there is an error persisting a conversation."""
  pass


class JSONConversationRepository(ConversationRepositoryInterface):
  """Using JSON file for persiting conversations data."""

  def __init__(self, file_path: str) -> None:
    self.__conversations = {}
    self.__file_path = file_path


  def get_or_create(self, id: UUID) -> Conversation:
    """Get or create a new conversation if it doesn't exist.

    :param UUID id: conversation id
    :return Conversation: conversation
    """
    # Load conversations from file if not already loaded
    if not self.__conversations:
      self.__load_conversations()

    # Get the conversation given its id
    try:
      conversation = self.__get_conversation_by_id(id)
    except ConversationNotFoundError:
      # If the conversation is not found, create a new one
      conversation = Conversation(id=id)
      self.__conversations[str(id)] = conversation.to_dict()

      # Save the new conversation to the file
      self.__save_conversations()

    return conversation


  def update(self, conversation: Conversation) -> None:
    """Update a conversation.

    :param Conversation conversation: conversation
    """
    # Load conversations from file if not already loaded
    if not self.__conversations:
      self.__load_conversations()

    # Update the conversation
    self.__conversations[str(conversation.id)] = conversation.to_dict()

    # Save the new conversation to the file
    self.__save_conversations()


  def list(self) -> list[Conversation]:
    """List all conversations.

    :return list[Conversation]: list of conversations
    """
    # Load conversations from file if not already loaded
    if not self.__conversations:
      self.__load_conversations()

    return [Conversation.from_dict(c) for c in self.__conversations.values()]


  # privates


  def __save_conversations(self) -> None:
    """Save conversations to JSON file.

    :raises ConversationJSONPersistenceError: if there is an error persisting the conversations
    """
    try:
      with open(self.__file_path, "w", encoding='utf-8') as f:
        json.dump({"conversations": self.__conversations}, f, indent=2)
    except Exception as e:
      raise ConversationJSONPersistenceError(
        f"Failed to save conversations to JSON file: {e}"
      )


  def __load_conversations(self) -> None:
    """Load conversations from JSON file.

    :raises ConversationJSONPersistenceError: if there is an error loading the conversations
    """
    try:
      with open(self.__file_path, "r", encoding='utf-8') as f:
        json_data = json.load(f)
        self.__conversations = json_data.get("conversations", {})
    except FileNotFoundError:
      self.__conversations = {}
    except json.JSONDecodeError as e:
      raise ConversationJSONPersistenceError(
        f"Failed to load conversations from JSON file: {e}"
      )


  def __get_conversation_by_id(self, id: UUID) -> Conversation:
    """Get the conversation given its id.

    :param UUID id: conversation id
    :return Conversation: conversation
    :raises ConversationNotFoundError: if the conversation is not found
    """
    key = str(id)
    if key not in self.__conversations:
      raise ConversationNotFoundError(f"Conversation with id {key} not found")

    # Return the conversation
    return Conversation.from_dict(self.__conversations[key])


#######################
# SQLite Repository
#######################


class SQLiteConversationRepository(ConversationRepositoryInterface):
  """Using SQLite database for persiting conversations data."""
  ...