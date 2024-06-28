import sys
import os

# Adjust path to the directory containing your Flask application
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app as application  # Adjust 'app' to match your actual Flask application object name

if __name__ == '__main__':
    application.run()
