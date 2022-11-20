import logging

LOG_FILE = "debug.log"

logging.basicConfig(format='%(asctime)s,%(msecs)d (%(filename)s, %(lineno)d) %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler(LOG_FILE, 'w+'),
                        logging.StreamHandler()
                    ],
                    level=logging.INFO)

logger = logging.getLogger("root")