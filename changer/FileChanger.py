# -*- coding: utf-8 -*-
import re
import os
import json
import collections
from tempfile import mkstemp
from shutil import move
from changer import Error
import logging

class FileChanger(object):

    def __init__(self, path_to_file="", config_path=""):
        self.config_path = config_path
        self.file = path_to_file
        self.host_address = None
        self.hostname = None
        self.file_content = None
        self.load_config()
        self.read_file()
        self.parse_file_content()

    def load_config(self):
        self.config = None
        with open(self.config_path) as file_handler:
            self.config = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)\
                .decode(file_handler.read().strip())
        self.hosts = self.config.get('hosts', [])
        if not self.file and self.config.get('client_init_path'):
            self.file = self.config.get('client_init_path')
        logging.info("Loaded {} host from config file".format(len(self.hosts)))

    def read_file(self):
        if self.file_not_exists():
            raise Error.FileNotFound('File "{}" not found'.format(self.file))
        with open(self.file) as file_handler:
            self.file_content = file_handler.read()

    def file_not_exists(self):
        return not os.path.exists(self.file)

    def parse_file_content(self):
        for line in self.file_content.split('\n'):
            valid_match = self.valid(line)
            if valid_match:
                self.host_address = valid_match.group(1)
                break
        for hostname, hostdata in self.hosts.items():
            if self.host_address == hostdata['address']:
                self.hostname = hostname
                for host, data in self.hosts.items():
                    data.checked = host == self.hostname
                break
        if not self.host_address:
            raise Error.SearchLineNotFound('line in config with key "host" not found')
        logging.info("Server {} with address {} active now".format(self.hostname, self.host_address))
        if not self.hostname:
            raise Error.SearchLineNotFound('Not found in valid hostname for {} in {}'\
                .format(self.host_address, self.config_path))

    def valid(self, line):
        return re.match(r'^(?!#)(?:\s*)host(?:\s*)=(?:\s*)([A-Za-z0-9\._]*)', line.strip())

    def valid_substring(self, line):
        return re.sub(r'^(?!#)(?:\s*)host(?:\s*)=(?:\s*)([A-Za-z0-9\._]*)',\
            'host = {}'.format(self.host_address), line.strip())+"\r\n"

    def switch_to_next_host(self):
        server_found = False
        new_server = None
        # host_lists = sum([(key, value['address']) for key, value in self.host_addresss.items()], ())
        for server_name in self.hosts:
            data = self.hosts[server_name]
            if server_found:
                new_server = server_name, data
                break
            elif server_name == self.host_address or data['address'] == self.host_address:
                server_found = True
        if not new_server:
            server_name = self.hosts.keys()[0]
            data = self.hosts[server_name]
            new_server = server_name, data
        server_name, data = new_server
        self.set_host_ip(data['address'])

    def set_host_ip(self, address):
        logging.info("Host {} changed to {}".format(self.host_address, address))
        self.host_address = address
        self.replace()

    def search_and_replace(self, hostname=''):
        logging.debug(json.dumps(self.hosts, indent=4))
        ipaddress = None
        is_ip = re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', hostname)
        if hostname in self.hosts:
            self.hosts[self.hostname].checked = False
            self.hosts[hostname].checked = True
            self.hostname = hostname
            self.set_host_ip(self.hosts[hostname]['address'])
        elif is_ip:
            ipaddress = is_ip.group(1)
            logging.info('this ip {} is valid'.format(ipaddress))
            self.set_host_ip(ipaddress)
        else:
            if ipaddress:
                raise Error.SetHostIpNotFound('IP address {} not found '\
                    .format(ipaddress))
            else:
                raise Error.SetHostIpNotFound('Hostname {} not found '\
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
