# coding: utf-8
'''Module with constants'''
from changer.dot_dict import DotDict

EXIT_CODE = DotDict(
    'SUCCESS',
    'WARNING',
    'ERROR'
)

LOG_LEVEL = DotDict({
    "CRITICAL": 50,
    "ERROR":    40,
    "WARNING":  30,
    "INFO":     20,
    "DEBUG":    10,
    "NOTSET":   0,
})
