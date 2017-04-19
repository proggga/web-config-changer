# coding: utf-8
"""
Module store current state and replace fields in file by request
"""
import collections
import json
import logging
import os
import re

from changer import Error
from changer import system_state


class FileChanger(object):
    '''Change file content and store current state'''

    def __init__(self, path_to_file="", config_path=""):
        self.config_path = config_path
        self.file = path_to_file
        self.state = system_state.SystemState()
        self.file_content = None
        self.config = None
        self.hosts = None
        self.load_config()
        self.read_file()
        self.parse_file_content()

    def load_config(self):
        '''load options from config'''
        with open(self.config_path) as file_handler:
            self.config = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)\
                .decode(file_handler.read().strip())
        self.hosts = self.config.get('hosts', [])
        if not self.file and self.config.get('client_init_path'):
            self.file = self.config.get('client_init_path')
        logging.info("Loaded %d host from config file", len(self.hosts))

    def read_file(self):
        '''read file or raise error'''
        if self.file_not_exists():
            raise Error.FileNotFound('File "{}" not found'.format(self.file))
        with open(self.file) as file_handler:
            self.file_content = file_handler.read()

    def file_not_exists(self):
        '''check if file not exists'''
        return not os.path.exists(self.file)

    def parse_file_content(self):
        '''parse file content and determine current state'''
        for line in self.file_content.split('\n'):
            valid_match_host = self.valid_host(line)
            valid_match_port = self.valid_port(line)
            if valid_match_host:
                self.state.host_address = valid_match_host.group(1)
            elif valid_match_port:
                self.state.host_port = valid_match_port.group(1)
        for hostname, hostdata in self.hosts.items():
            if self.state.host_address == hostdata['address']:
                self.state.hostname = hostname
                for host, data in self.hosts.items():
                    data.checked = host == self.state.hostname
                break
        if not self.state.host_address:
            message = 'line in config with key "host" not found'
            raise Error.SearchLineNotFound(message)
        logging.info("Server %s with address %s active now",
                     self.state.hostname, self.state.host_address)
        if not self.state.hostname:
            message = "config have no '{}' record, replacing by first" \
                      "record in config".format(self.state.host_address)
            logging.info(message)
            self.switch_to_next_host()

    @staticmethod
    def valid_host(line):
        '''check if line is valid 'host' line like: ^ host = 172.16.0.15 $ '''
        return re.match(r'^(?!#)(?:\s*)host(?:\s*)=(?:\s*)([A-Za-z0-9\._]*)',
                        line.strip())

    @staticmethod
    def valid_port(line):
        '''check if line is valid 'port' line like: ^ port = 8000 $ '''
        return re.match(r'^(?!#)(?:\s*)port(?:\s*)=(?:\s*)([0-9\._]*)',
                        line.strip())

    def valid_substring(self, line):
        '''check if valid and replace by current host_address value'''
        return re.sub(r'^(?!#)(?:\s*)host(?:\s*)=(?:\s*)([A-Za-z0-9\._]*)',
                      'host = {}'.format(self.state.host_address),
                      line.strip())

    def valid_substring_port(self, line):
        '''check if valid and replace by current port value'''
        return re.sub(r'^(?!#)(?:\s*)port(?:\s*)=(?:\s*)([0-9]*)',
                      'port = {}'.format(self.state.host_port), line.strip())

    def switch_to_next_host(self):
        '''determine which host is next by order and switch config to it'''
        server_found = False
        new_server = None
        for server_name in self.hosts:
            data = self.hosts[server_name]
            if server_found:
                message = "replacing by next {} {}".format(server_name, data)
                logging.debug(message)
                new_server = server_name, data
                break
            elif (server_name == self.state.host_address or
                  data['address'] == self.state.host_address):
                debug_message = "found new server {} {} {}" \
                                .format(server_name,
                                        data,
                                        self.state.host_address)
                logging.debug(debug_message)
                server_found = True
        if not new_server:
            logging.debug("if not new_server set by default")
            server_name = self.hosts.keys()[0]
            data = self.hosts[server_name]
            new_server = server_name, data
        server_name, data = new_server
        self.state.hostname = server_name
        self.set_host_ip(data['address'])
        self.set_host_port(data['port'])

    def set_host_ip(self, address):
        '''set host ip address and replace config'''
        logging.info("Host %s changed to %s",
                     self.state.host_address, address)
        self.state.host_address = address
        self.replace()

    def set_host_port(self, port):
        '''set host port and replace config'''
        info_message = "Port {} changed to {}" \
                       .format(self.state.host_port, port)
        logging.info(info_message)
        self.state.host_port = port
        self.replace()

    def search_and_replace(self, hostname=''):
        '''search host by hostname and replace config'''
        logging.debug(json.dumps(self.hosts, indent=4))
        ipaddress = None
        is_ip = re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', hostname)
        if hostname in self.hosts:
            self.hosts[self.state.hostname].checked = False
            self.hosts[hostname].checked = True
            self.state.hostname = hostname
            self.set_host_ip(self.hosts[hostname]['address'])
            self.set_host_port(self.hosts[hostname]['port'])
        elif is_ip:
            ipaddress = is_ip.group(1)
            logging.info('this ip %s is valid', ipaddress)
            self.set_host_ip(ipaddress)
        else:
            if ipaddress:
                raise Error.SetHostIpNotFound('IP address {} not found '
                                              .format(ipaddress))
            else:
                raise Error.SetHostIpNotFound('Hostname {} not found '
                                              .format(hostname))

    @staticmethod
    def append_new_line(line):
        '''apend line if it not empty line'''
        if line not in ['\r', '']:
            return '\r\n'
        else:
            return ''

    def replace(self):
        '''rewrite to file new config replaced by regexps'''
        with open(self.file, 'r+') as file_handler:
            file_content = file_handler.read()
            file_handler.seek(0)
            for line in file_content.split('\n'):
                newline = self.valid_substring(line)
                newline = self.valid_substring_port(newline)
                file_handler.write(newline + self.append_new_line(line))
            file_handler.truncate()
            file_handler.close()
