import os
import sys
from loguru import logger

# Create logs folder automatically
os.makedirs("logs", exist_ok=True)

logger.remove()

# Log to terminal
logger.add(
    sys.stdout,
    level="INFO",
    colorize=True
)

# Log to file
logger.add(
    "logs/scraper.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    encoding="utf-8"
)