from changer.enum import Enum

EXIT_CODE = Enum(
    'SUCCESS',
    'WARNING',
    'ERROR'
)

LOG_LEVEL = Enum({
    "CRITICAL": 50,
    "ERROR":    40,
    "WARNING":  30,
    "INFO":     20,
    "DEBUG":    10,
    "NOTSET":   0,
})
