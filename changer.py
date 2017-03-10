import re
import os
from errors import FileNotFoundException
from errors import SearchLineNotFound

class ClientFileChanger(object):

    def __init__(self, path_to_file):
        self.file = path_to_file
        self.host = None
        self.file_content = None
        self.read_file()
        self.parse_file_content()

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
                self.host = valid_match.group(1)
                break
        if not self.host:
            raise SearchLineNotFound('line started from "host" not found')

    def valid(self, line):
        return re.match(r'^\s*host\s*=\s*(.*)(\s*?)', line.strip())

from changer import ClientFileChanger
a = ClientFileChanger('client.ini')
a.file
a.host
