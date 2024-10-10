from tests import reader


def test_reader_info():
    # Check that no exception is thrown when getting reader info
    reader.GetReaderInfo()


def test_device_caps():
    # Check that no exception is thrown when getting device caps
    reader.GetDeviceCaps()
