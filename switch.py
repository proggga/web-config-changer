#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from changer.FileChanger import FileChanger
from changer import Error, log

log.set_logging()

changer = FileChanger(config_path='config.json')

if len(sys.argv) > 1:
    try:
        changer.search_and_replace(sys.argv[1])
    except Error.SetHostIpNotFound as ex:
        print str(ex)
else:
    changer.switch_to_next_host()