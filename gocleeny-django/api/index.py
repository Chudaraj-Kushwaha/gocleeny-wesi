from django.core.wsgi import get_wsgi_application
import os
import sys

# Add the project directory to the sys.path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gocleeny.settings')

# Get the WSGI application
app = get_wsgi_application()

