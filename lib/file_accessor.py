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

    def file_format_valid(self):
        """
        input file format:
        it should not be empty file
        it should be tsv format, and should have as latest two column
        :return:
        """
        try:
            with open(self.file_path, 'r') as open_file:
                lines = open_file.readlines()
                if len(lines) < 1:
                    return False
                for line in lines:
                    if line:
                        sentence_list = line.split('\t')
                        if len(sentence_list) < 2:
                            return False
            return True
        except:
            return False

    def read_file(self):
        try:
            with open(self.file_path, 'r') as open_file:
                lines = [line.strip() for line in open_file.readlines()]
                return lines
        except:
            raise Exception('invalid file')
