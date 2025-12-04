"""Application factory function define."""

import os
from flask import Flask

from src.application.services.conversation import ConversationService
from src.infra.repository import JSONConversationRepository
from src.infra.llm_adapter import LLMCohereAdapter
from src.ui.api.flask_api import config


def init_conversation_service(app):
  # Setup the conversation service
  llm_provider = LLMCohereAdapter({
    "cohere_api_key": app.config["COHERE_API_KEY"],
    "cohere_model": app.config["COHERE_MODEL"],
    "cohere_max_messages": app.config["COHERE_MAX_MESSAGES"],
    "system_message": app.config["SYSTEM_MESSAGE"],
  })
  conversation_repository = JSONConversationRepository(
    app.config["JSON_DATABASE_FILE"]
  )
  conversation_service = ConversationService(
    llm_provider, conversation_repository
  )

  app.extensions["conversation_service"] = conversation_service


def create_app(env: str = ""):
  """Factory function to create the application."""
  # Get the instance path
  instance_path = os.path.join(
    os.path.dirname(os.path.abspath(os.path.dirname(__file__))),
    'instance'
  )

  # Create the application
  app = Flask(__name__,
              instance_relative_config=True,
              instance_path=instance_path)

  # Load configuration settings
  env_name = env or os.environ.get('FLASK_ENV', 'development')
  if env_name == 'production':
    app.config.from_object(config.ProductionConfig)
  elif env_name == 'testing':
    app.config.from_object(config.TestingConfig)
  else:
    app.config.from_object(config.DevelopmentConfig)

  # Look for config.cfg inside the 'instance' folder.
  try:
    app.config.from_pyfile('config.cfg', silent=True)
  except FileNotFoundError:
    pass

  # Ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # Initialize conversation service
  init_conversation_service(app)

  # Register blueprints
  from src.ui.api.flask_api.app.chatbot import routes
  app.register_blueprint(routes.chatbot_bp)

  return app
