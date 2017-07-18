#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os


class FileAccessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def file_exit_valid(self):
        if self.file_path and os.path.isfile(self.file_path):
            return True
        else:
            return False

    def read_file(self):
        try:
            with open(self.file_path, 'r') as open_file:
                lines = [line.strip().encode('utf-8') for line in open_file.readlines()]
                return lines
        except:
            raise Exception('invalid file')
