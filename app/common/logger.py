import json
import logging.config
import logging.handlers

config = json.load(open('app/logging.json'))
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

logger.info("logger Ready Successes!")


def getLogger(name):
    return logging.getLogger(name)

