import sys

from loguru import logger
from datetime import datetime
import os

from . import config

# Set logger level
logger.remove()
logger.add(sys.stderr, level=config.LOG_LEVEL, colorize=True, format=config.LOG_FORMAT)

# Create file handler
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)

current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
log_file = os.path.join(log_folder, f'{current_time}.log')

# Add file handler
logger.add(log_file, rotation="500 MB", level=config.LOG_LEVEL, colorize=False, format=config.LOG_FORMAT)