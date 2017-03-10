import re
import os
import json
import collections
from errors import FileNotFoundException
from errors import SearchLineNotFound

class ClientFileChanger(object):

    def __init__(self, path_to_file='client.ini', config_path='config.json'):
        self.config_path = config_path
        self.load_config()
        self.file = path_to_file
        self.host = None
        self.file_content = None
        self.read_file()
        self.parse_file_content()

    def load_config(self):
        self.hosts = None
        with open(self.config_path) as file_handler:
            self.hosts = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)\
                .decode(file_handler.read().strip())
# with open('config.json') as file_handler:
#     hosts = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)\
#         .decode(file_handler.read().strip())
    def read_file(self):
        if self.file_not_exists():
            raise FileNotFoundException('File "{}" not found'.format(self.file))
        with open(self.file) as file_handler:
            self.file_content = file_handler.read()

    def file_not_exists(self):
        return not os.path.exists(self.file)

    def parse_file_content(self):
        for line in self.file_content.split('\n'):
            valid_match = self.valid(line)
            if valid_match:
                print "found line, saving: {}".format(line)
                print valid_match.groups()
                self.host = valid_match.group(1)
                break
        if not self.host:
            raise SearchLineNotFound('line started from "host" not found')

    def valid(self, line):
        return re.match(r'^(?!#)(?:\s*?)host(?:\s*?)=\s*([A-Za-z0-9\._]*)', line.strip())

    def switch_to_next_host(self):
        server_found = False
        new_server = None
        # host_lists = sum([(key, value['address']) for key, value in self.hosts.items()], ())
        for server_name in self.hosts:
            data = self.hosts[server_name]
            if server_found:
                new_server = server_name, data
                break
            elif server_name == self.host or data['address'] == self.host:
                server_found = True
        if not new_server:
            server_name = self.hosts.keys()[0]
            data = self.hosts[server_name]
            new_server = server_name, data
        return new_server

    def replace_by(self, server_name, data):
        pass
