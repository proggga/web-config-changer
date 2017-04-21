#!/usr/bin/env python
# coding: utf-8
'''
Web application point of entry
by proggga
'''

from changer.constants import LOG_LEVEL
from changer import log
from changer.webapp import APP

log.set_logging(LOG_LEVEL.INFO)

if __name__ == '__main__':
    APP.run(host='0.0.0.0')
