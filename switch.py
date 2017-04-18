#!/usr/bin/env python
# coding: utf-8
'''script with switch to next host'''
import logging
import sys

from changer.constants import EXIT_CODE
from changer.constants import LOG_LEVEL
from changer import Error
from changer.FileChanger import FileChanger
from changer import log

log.set_logging(LOG_LEVEL.INFO)

CHANGER = FileChanger(config_path='config.json')

if len(sys.argv) > 1:
    try:
        CHANGER.search_and_replace(sys.argv[1])
    except Error.SetHostIpNotFound as ex:
        logging.error("Error is %s", ex)
        exit(EXIT_CODE.ERROR)
else:
    CHANGER.switch_to_next_host()
