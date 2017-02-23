import logging
import time

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Create a log handler
handler = logging.FileHandler('../logs/logs'+time.strftime("%d_%m_%y_%H_%M_%S")+'.txt')
handler.setLevel(logging.DEBUG)

# Format Logs
formattor = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formattor)

# Link handler with Logger
logger.addHandler(handler)