import os
import pytest
from src.ui.api.flask_api.app import create_app


@pytest.fixture(name='flask_app', scope='session')
def flask_app_fixture():
  """Creates a Flask app instance configured for testing."""

  app = create_app(env="testing")

  # Set up application context
  with app.app_context():
    yield app

    # Remove the database file
    if os.path.exists(app.config["JSON_DATABASE_FILE"]):
      os.remove(app.config["JSON_DATABASE_FILE"])


@pytest.fixture(name='web_client', scope='function')
def web_client_fixture(flask_app):
  """Creates a test client for the application."""
  return flask_app.test_client()
