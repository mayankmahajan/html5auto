import logging

# Create a logger
resultlogger = logging.getLogger(__name__)
resultlogger.setLevel(logging.DEBUG)


# Create a log handler
handler = logging.FileHandler('../logs/result.html')
handler.setLevel(logging.DEBUG)

# Format Logs
formattor = logging.Formatter("%(asctime)s - %(message)s")
# formattor = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formattor)

# Link handler with Logger
resultlogger.addHandler(handler)