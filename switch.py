#!/usr/bin/env python
# -*- coding: utf-8 -*-
from changer.constants import EXIT_CODE
from changer.constants import LOG_LEVEL
from changer import Error
from changer.FileChanger import FileChanger
from changer import log
import sys

log.set_logging(LOG_LEVEL.INFO)

changer = FileChanger(config_path='config.json')

if len(sys.argv) > 1:
    try:
        changer.search_and_replace(sys.argv[1])
    except Error.SetHostIpNotFound as ex:
        print(str(ex))
        exit(EXIT_CODE.ERROR)
else:
    changer.switch_to_next_host()
