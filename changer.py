import re
import os
import json
import collections
from tempfile import mkstemp
from shutil import move
from errors import FileNotFound
from errors import SearchLineNotFound
from errors import SetHostIpNotFound

class FileChanger(object):

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
        print "Loaded {} host from config file".format(len(self.hosts))

    def read_file(self):
        if self.file_not_exists():
            raise FileNotFound('File "{}" not found'.format(self.file))
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
        print "Current address is {}".format(self.host)
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
        self.set_host_ip(data['address'])

    def set_host_ip(self, ipaddress):
        print "Host {} changed to {}".format(self.host, ipaddress)
        self.host = ipaddress
        self.replace()

    def search_and_replace(self, hostname=''):
        ipaddress = None
        reg = re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', hostname)
        if reg:
            ipaddress = reg.group(1)
            print('this ip {} is valid'.format(ipaddress))
            self.set_host_ip(ipaddress)
        elif hostname in self.hosts:
            self.set_host_ip(self.hosts[hostname]['address'])
        else:
            if ipaddress:
                raise SetHostIpNotFound('IP address {} not found '\
                    .format(ipaddress))
            else:
                raise SetHostIpNotFound('Hostname {} not found '\
                    .format(hostname))

    def replace(self):
        file_handler, absolute_path = mkstemp()
        with open(absolute_path, 'w') as temp_file:
            with open(self.file) as current_file:
                for line in current_file:
                    temp_file.write(self.valid_substring(line))
        os.close(file_handler)
        os.remove(self.file)
        move(absolute_path, self.file)
