import logging

DEBUG_LOG_FILE = "debug.log"
INFO_LOG_FILE = "info.log"

logger = logging.getLogger("root")


formatter = logging.Formatter(
    '%(asctime)s,%(msecs)d (%(filename)s, %(lineno)d) %(name)s %(levelname)s %(message)s')

logger.setLevel(logging.DEBUG)

file_handler_info = logging.FileHandler(INFO_LOG_FILE, 'w+')
file_handler_info.setLevel(logging.INFO)
file_handler_info.setFormatter(formatter)

file_handler = logging.FileHandler(DEBUG_LOG_FILE, 'w+')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(file_handler_info)
logger.addHandler(console_handler)