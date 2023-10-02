import logging


def create_logger(name, listen_type=logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(listen_type)

    stream = logging.StreamHandler()
    stream.setLevel(listen_type)

    formatter = logging.Formatter("%(asctime)s %(levelname)-10s %(message)s")
    stream.setFormatter(formatter)

    logger.addHandler(stream)
    return logger
