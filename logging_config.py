import logging

logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()

logger.addHandler(handler)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

handler.setFormatter(formatter)

logger.info("Logging system started")