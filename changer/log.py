def set_logging():
    import logging
    FORMAT = '%(asctime)s %(module)s:\t %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger()
    logger.setLevel(20)
