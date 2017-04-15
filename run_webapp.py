#!/usr/bin/env python

from changer.constants import LOG_LEVEL
from changer import log
from changer.webapp import app

log.set_logging(LOG_LEVEL.INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
