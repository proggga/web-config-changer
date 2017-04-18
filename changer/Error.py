# coding: utf-8
'''Module with errors classes'''


class FileNotFound(Exception):
    '''File not found Exception'''
    pass


class SearchLineNotFound(Exception):
    '''Search line not found Exception'''
    pass


class SetHostIpNotFound(Exception):
    '''Not found ip when setting new host Exception'''
    pass
