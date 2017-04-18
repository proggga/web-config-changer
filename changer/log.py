# coding: utf-8
'''Logging init'''


def set_logging(log_level):
    '''set loggin with level for all project/app'''
    import logging
    log_format = '%(asctime)s %(module)s:\t %(message)s'
    logging.basicConfig(format=log_format)
    logger = logging.getLogger()
    logger.setLevel(log_level)
