#!/usr/bin/env python
# -*- coding: utf-8 -*-
from changer import ClientFileChanger

changer = ClientFileChanger(path_to_file='client.ini', config_path='config.json')

print changer.switch_to_next_host()
# print new_server
# else:
#     print "file not in config, replacing, by first one"
#     for key, value in hosts.items():
#         changer.replace_by(key, value)
#         break
