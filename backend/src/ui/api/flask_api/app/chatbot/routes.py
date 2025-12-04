"""
Module for chatbot routes.

This module contains all endpoints related to /conversations url.
"""

from uuid import UUID

from flask import Blueprint, current_app, request


# Setup a blueprint
chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/conversations")


# Endpoints

@chatbot_bp.route("", methods=["POST"])
def create_conversation():
  """Create a new conversation."""
  conversation_service = current_app.extensions["conversation_service"]
  conversation_id = conversation_service.create_conversation()
  return {"conversation_id": str(conversation_id)}


@chatbot_bp.route("/<uuid:conversation_id>", methods=["GET"])
def get_conversation_history(conversation_id):
  """Get the conversation history."""
  conversation_service = current_app.extensions["conversation_service"]
  history = conversation_service.get_conversation_history(conversation_id)
  return {"history": [m.to_dict() for m in history]}


@chatbot_bp.route("/<uuid:conversation_id>", methods=["POST"])
def add_message_to_conversation(conversation_id):
  """Add a message to the conversation."""
  # Get message from request body
  message = request.json["message"]

  # Add message to conversation
  conversation_service = current_app.extensions["conversation_service"]
  response = conversation_service.send_message(
    conversation_id, message
  )
  return {"response": response}


@chatbot_bp.route("/<uuid:conversation_id>", methods=["DELETE"])
def reset_conversation(conversation_id):
  """Reset the conversation history."""
  conversation_service = current_app.extensions["conversation_service"]
  conversation_service.reset_conversation(conversation_id)
  return {"message": "Conversation has been reset"}


@chatbot_bp.route("", methods=["GET"])
def list_conversations():
  """List all conversations."""
  conversation_service = current_app.extensions["conversation_service"]
  conversations = conversation_service.list_conversations()
  return {"conversations": [c.to_dict() for c in conversations]}
