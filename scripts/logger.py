import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Create a log handler
handler = logging.FileHandler('/Users/mayank.mahajan/PycharmProjects/html5automation1/logs/logs.txt')
handler.setLevel(logging.INFO)

# Format Logs
formattor = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formattor)

# Link handler with Logger
logger.addHandler(handler)