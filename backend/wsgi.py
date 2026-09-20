"""
WSGI entrypoint for production server deployment (Gunicorn / Waitress / uWSGI)
"""
import os
import sys

# Ensure application directory is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
