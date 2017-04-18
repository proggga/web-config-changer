# coding: utf-8
'''
DotDict, used like dict with access to fields by dots (like 'object.value')
'''
from collections import OrderedDict


class DotDict(OrderedDict):
    '''DotDict which get dict for init'''

    def __init__(self, *args):
        data = OrderedDict()
        if len(args) == 1:
            keys = args[0]
            if isinstance(keys, list) or isinstance(keys, tuple):
                for index, key in enumerate(keys):
                    data[key] = index
            else:
                data = keys
        else:
            for index, key in enumerate(args):
                data[str(key)] = index
        super(DotDict, self).__init__(data)

    def __getattr__(self, name):
        '''access to dict by dots'''
        if name in self:
            return self[name]
        raise AttributeError
