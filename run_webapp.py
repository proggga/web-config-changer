#!/usr/bin/env python

from changer.webapp import app
from changer import log
from changer.constants import LOG_LEVEL

log.set_logging(LOG_LEVEL.INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
