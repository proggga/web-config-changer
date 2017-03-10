import re
import os
import json
import collections
from tempfile import mkstemp
from shutil import move
from errors import FileNotFound
from errors import SearchLineNotFound
from errors import SetHostIpNotFound

class ClientFileChanger(object):

    def __init__(self, path_to_file='client.ini', config_path='config.json'):
        self.config_path = config_path
        self.file = path_to_file
        self.host = None
        self.file_content = None
        self.load_config()
        self.read_file()
        self.parse_file_content()

    def load_config(self):
        self.hosts = None
        with open(self.config_path) as file_handler:
            self.hosts = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)\
                .decode(file_handler.read().strip())

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
                self.host = valid_match.group(1)
                break
        if not self.host:
            raise SearchLineNotFound('line in config with key "host" not found')

    def valid(self, line):
        return re.match(r'^(?!#)(?:\s*)host(?:\s*)=(?:\s*)([A-Za-z0-9\._]*)', line.strip())

    def valid_substring(self, line):
        return re.sub(r'^(?!#)(?:\s*)host(?:\s*)=(?:\s*)([A-Za-z0-9\._]*)',\
            'host = {}'.format(self.host), line.strip())+"\r\n"

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
        server_name, data = new_server
        self.host = data['address']
        self.replace()

    def set_host(self, hostname=None, ipaddress=None):
        iphost_list = sum([(key, value['address']) for key, value in self.hosts.items()], ())
        if hostname in iphost_list:
            host_index = iphost_list.index(hostname)
            self.host = iphost_list[host_index+1]
        elif ipaddress in iphost_list:
            self.host = ipaddress
        else:
            raise SetHostIpNotFound('Ip addr ({}) or hostname ({}) not found '\
                .format(hostname, ipaddress))
        self.replace()

    def replace(self):
        file_handler, absolute_path = mkstemp()
        with open(absolute_path, 'w') as temp_file:
            with open(self.file) as current_file:
                for line in current_file:
                    temp_file.write(self.valid_substring(line))
        os.close(file_handler)
        os.remove(self.file)
        move(absolute_path, self.file)
