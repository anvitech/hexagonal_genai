from uuid import UUID
import pytest


@pytest.mark.unit
def test_crud_operations_with_success(web_client):
  """The create conversation endpoints should returns a correct response."""

  # --- Test the create_conversation endpoint ---

  # Create a conversation
  response = web_client.post('/conversations')

  # Check the Status Code
  assert response.status_code == 200

  # Check the response data
  assert "conversation_id" in response.json
  assert UUID(response.json["conversation_id"])


  # --- Test the add_message_to_conversation endpoint ---

  # Get the conversation id
  conversation_id = response.json["conversation_id"]

  # Add a message to the conversation
  message = "Hello, World!"
  response = web_client.post(
    f'/conversations/{conversation_id}',
    json={"message": message}
  )

  # Check the Status Code
  assert response.status_code == 200

  # Check the response data
  assert "response" in response.json
  assert isinstance(response.json["response"], str)
  assert len(response.json["response"]) > 0


  # --- Test the get_conversation_history endpoint ---

  # Get the conversation history
  response = web_client.get(f'/conversations/{conversation_id}')

  # Check the Status Code
  assert response.status_code == 200

  # Check the response data
  assert "history" in response.json
  assert isinstance(response.json["history"], list)
  assert len(response.json["history"]) > 0


  # --- Test the list_conversations endpoint ---

  # List the conversations
  response = web_client.get('/conversations')

  # Check the Status Code
  assert response.status_code == 200

  # Check the response data
  assert "conversations" in response.json
  assert isinstance(response.json["conversations"], list)
  assert len(response.json["conversations"]) > 0


  # --- Test the reset_conversation endpoint ---

  # Reset the conversation
  response = web_client.delete(f'/conversations/{conversation_id}')

  # Check the Status Code
  assert response.status_code == 200


def test_404_not_found(web_client):
  """Tests that a non-existent route returns 404."""
  response = web_client.get('/nonexistent_route')
  assert response.status_code == 404
