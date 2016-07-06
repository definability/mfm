from os.path import join

TEST_DATA_FOLDER = 'data'


def get_datafile_path(filename):
    return join(TEST_DATA_FOLDER, filename)
