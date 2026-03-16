import logging

def setup_logging(name):

    logging.basicConfig(
        level=logging.INFO,  # минимальный уровень логирования
        format='%(asctime)s | %(levelname)-8s | %(name)-12s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger(name)

    return logger