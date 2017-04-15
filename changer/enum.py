from collections import OrderedDict


class Enum(OrderedDict):
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
        super(Enum, self).__init__(data)

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError
