#!/usr/bin/env python

from changer.webapp import app
from changer import log

log.set_logging()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
