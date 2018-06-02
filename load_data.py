import json


class Data:
    def __init__(self, history_set_name):
        self.file_error = 0
        self.history_set_name = history_set_name
        self.index_file = 'index_' + history_set_name
        try:
            self.data_stream = open("../data/" + self.history_set_name)
            self.data = json.load(self.data_stream)
        except IOError as e:
            print (e)
            self.file_error = 1
            print ("I/O Error - Not Opening File")
            return
        # try:
        #     open('search_index/' + self.index_file, 'w')
        # except Exception as e:
        #     pass

        self.no_of_segments = 0

    def is_file(self):
        if self.file_error:
            return True
        else:
            return False

    def get_count(self):
        return len(self.data)

    # get number of segments data is divided into
    def get_segment_count(self):
        self.segmentation()
        return self.no_of_segments

    # get number of objects(history links) in each segment
    def get_segment_details(self):
        for x in self.segmentation():
            print len(x)

    # def extract_links(self):

    def segmentation(self):
        segments = list(chunks(self.data))
        self.no_of_segments = len(segments)
        return segments

    def get_index_file(self):
        return self.index_file


# function to divide data array into chunks based on size of data set
# this allows for multi-threading and processing of data
def chunks(base_array):
    length = len(base_array)
    if length <= 100:
        n_chunks = 10
    elif 100 < length <= 1000:
        n_chunks = 100
    else:
        n_chunks = 1000

    for i in range(0, len(base_array), n_chunks):
        yield base_array[i:i + n_chunks]


if __name__ == '__main__':
    test = Data()
    print test.get_segment_details()