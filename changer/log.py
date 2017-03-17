def set_logging(log_level):
    import logging
    FORMAT = '%(asctime)s %(module)s:\t %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger()
    logger.setLevel(log_level)
