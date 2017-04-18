# coding: utf-8
'''Module with class SystemState container'''
from changer.dot_dict import DotDict


class SystemState(DotDict):
    '''System current state container'''

    def __init__(self, address=None, port=None, hostname=None):
        init_dict = {
            'address': address,
            'port': port,
            'hostname': hostname,
        }
        super(SystemState, self).__init__(init_dict)
