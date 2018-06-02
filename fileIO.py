# -*- coding: utf-8 -*-
import json
import random
import string
import os.path

TARGET_INDEX_FILE_URL_INDEX = 'indices'


class FileIO:
    def __init__(self, filename):
        self.filename = filename

    def isFile(self):
        try:
            f = open(self.filename, 'w')
            f.close()
            return True
        except Exception as e:
            return False

    def create_file(self, data):
        try:
            push_data = {TARGET_INDEX_FILE_URL_INDEX: []}
            push_data[TARGET_INDEX_FILE_URL_INDEX].append(data)
            with open(self.filename, 'w') as outfile:
                json.dump(push_data, outfile, indent=4)
                outfile.close()
        except Exception as e:
            print e
            return

    def read_file(self):
        try:
            with open(self.filename) as jsonfile:
                response = json.load(jsonfile)
                jsonfile.close()
                return response
        except Exception as e:
            print e
            return

    def update_file(self, data):
        try:
            tmp_data = self.read_file()
            tmp_data[TARGET_INDEX_FILE_URL_INDEX].append(data)
            with open(self.filename, 'w') as outfile:
                json.dump(tmp_data, outfile, indent=4)
                outfile.close()
            return self.read_file()
        except Exception as e:
            print e
            return

    def delete_file(self):
        pass

    def __delete__(self, instance):
        # close all file_objects to release resources
        pass
