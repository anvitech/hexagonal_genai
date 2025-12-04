import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  """Base configuration class."""

  SECRET_KEY = os.environ.get('SECRET_KEY', 'development-key')

  # Set the database file path
  JSON_DATABASE_FILE = os.path.join(basedir, "db.json")

  # Setup LLM provider config
  COHERE_MODEL = 'command-a-03-2025'
  COHERE_MAX_MESSAGES = 100
  SYSTEM_MESSAGE = "You are a helpful assistant. You respond in concise sentences."


class ProductionConfig(Config):
  """Configuration specific to the production environment."""
  DEBUG = False
  TESTING = False

  # Set the database file path
  JSON_DATABASE_FILE = os.path.join(basedir, "prod_db.json")


class DevelopmentConfig(Config):
  """Configuration specific to the development environment."""
  DEBUG = True
  TESTING = False
  SECRET_KEY = 'development-key'

  # Set the database file path
  JSON_DATABASE_FILE = os.path.join(basedir, "dev_db.json")


class TestingConfig(Config):
  """Configuration specific to the testing environment."""
  TESTING = True

  # Set the database file path
  JSON_DATABASE_FILE = os.path.join(basedir, "test_db.json")

  WTF_CSRF_ENABLED = False
