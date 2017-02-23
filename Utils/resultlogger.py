import logging
import time

# Create a logger
resultlogger = logging.getLogger(__name__)
resultlogger.setLevel(logging.DEBUG)


# Create a log handler
handler = logging.FileHandler('../logs/result'+time.strftime("%d_%m_%y_%H_%M_%S")+'.html')
handler.setLevel(logging.DEBUG)

# Format Logs
formattor = logging.Formatter("%(asctime)s  -  %(message)s","%Y-%m-%d %H:%M")
# formattor = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formattor)

# Link handler with Logger
resultlogger.addHandler(handler)