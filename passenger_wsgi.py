import sys, os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# get python directory from .env file
PYTHON_DIR = os.getenv('PYTHON_DIR', '')

if sys.executable != PYTHON_DIR:
    os.execl(PYTHON_DIR, PYTHON_DIR, *sys.argv)

# Add the current directory to Python path
sys.path.append(os.getcwd())

# Import FastAPI app and convert to WSGI
from main import app
from asgiref.wsgi import WsgiToAsgi

# Convert FastAPI (ASGI) app to WSGI for Passenger
application = WsgiToAsgi(app)
