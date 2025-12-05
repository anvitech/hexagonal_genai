"""Entry point for Flask application."""

import os
import sys


# Add backend resource folder to sys path
basedir = os.path.abspath(__file__)
backend_source_path = os.path.dirname(os.path.dirname(
  os.path.dirname(os.path.dirname(os.path.dirname(basedir)))
))
if backend_source_path not in sys.path:
    sys.path.insert(0, backend_source_path)


from app import create_app
from flask_cors import CORS

# Create the application
app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
  # For development
  app.run(debug=True)
