import logging
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler
import os


PROJECT_ROOT_DIRECTORY = Path(__file__).parent.parent.parent.absolute()
LOGS_DIR = PROJECT_ROOT_DIRECTORY / 'logs'

# Create directory if it doesn't exist (pathlib way)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Create log file path using pathlib
log_file = LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"

# Get log level from environment
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
log_level_mapping = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR
}

# Create rotating file handler
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=10*1024*1024,  # 10MB per file
    backupCount=5,          # Keep 5 files (total 50MB)
    encoding='utf-8'
)

logging.basicConfig(
    level=log_level_mapping.get(log_level, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        file_handler,
        logging.StreamHandler()  # Also log to console
    ]
)

def create_logger(logger_name):
    return logging.getLogger(logger_name)