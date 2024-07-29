from loguru import logger

logger.add(
    "logs/app.log",
    level="DEBUG",
    rotation="10 MB",
    format="{time:DD-MM-YYYY hh:mm:ss A} - {level} - {message}",
)