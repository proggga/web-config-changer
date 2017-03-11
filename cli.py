#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from changer import FileChanger
from errors import SetHostIpNotFound

changer = FileChanger(path_to_file='client.ini', config_path='config.json')

if len(sys.argv) > 1:
    try:
        changer.search_and_replace(sys.argv[1])
    except SetHostIpNotFound as ex:
        print str(ex)
else:
    changer.switch_to_next_host()
