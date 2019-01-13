import logging


def get_logger(name):
    logger = logging.getLogger(name)
    frmt = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=frmt)
    logger.setLevel(logging.INFO)
    return logger
