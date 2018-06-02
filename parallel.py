import threading
import load_data
import extraction
import os.path
from fileIO import FileIO

DATA_SOURCE = '../data/'


# Multi-threading and parallel processing of chunks of data
class ProcessThread(threading.Thread):
    def __init__(self, url_list, data):
        threading.Thread.__init__(self)
        self.url_list = url_list

    def run(self):
        for url_object in self.url_list:
            extract_object = extraction.Extraction(url_object)
            url_object['word_index'] = extract_object.get_text()

            # try:
            #     # open('search_index/' + data.index_file, 'w')
            #     file = FileIO('search_index/' + data.index_file)
            #     print file.create_file(url_object)
            # except:
            #     file = FileIO('search_index/' + data.index_file)
            #     print file.create_file(url_object)

            # file = FileIO('search_index/' + data.get_index_file())
            # print file.create_file(url_object)
            # f = open(os.path.dirname(__file__) + '/../data.yml')
            if os.path.isfile('../search_index/' + data.index_file):
                file = FileIO('../search_index/' + data.index_file)
                file.update_file(url_object)
            else:
                file = FileIO('../search_index/' + data.index_file)
                file.create_file(url_object)

            # url_object[]


if __name__ == '__main__':
    # data = load_data.Data('test.json')
    # if not data.is_file():
    #     data_array = data.segmentation()
    #     # print len(data_array)
    #     for segment in data_array:
    #         ProcessThread(segment, data).start()
    for file in os.listdir(DATA_SOURCE):
        if file.endswith(".json") or file.endswith(".txt"):
            data = load_data.Data(file)
            if not data.is_file():
                data_array = data.segmentation()
                for segment in data_array:
                    ProcessThread(segment, data).start()

