from os.path import dirname, abspath, join

TEST_DATA_FOLDER = dirname(abspath(__file__))


def get_datafile_path(filename):
    return join(TEST_DATA_FOLDER, filename)
