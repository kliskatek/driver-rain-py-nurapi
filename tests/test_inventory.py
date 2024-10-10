import time

from src.nurapi import NurInventoryStreamData
from tests import reader


def test_simple_inventory():
    tag_data = None
    # Trigger a simple inventory
    inventory_response = reader.SimpleInventory()

    if inventory_response.num_tags_mem > 0:
        # Fetch read tags to tag buffer including metadata
        tag_count = reader.FetchTags(include_meta=True)

        # Get data of read tags
        for idx in range(tag_count):
            tag_data = reader.GetTagData(idx=idx)

    # Clear tag buffer
    reader.ClearTags()

    assert tag_data is not None


def test_inventory_stream():
    tag_data = None

    # Define callback
    def my_callback(inventory_stream_data: NurInventoryStreamData):
        nonlocal tag_data
        # If stream stopped, restart
        if inventory_stream_data.stopped:
            reader.StartInventoryStream(rounds=10, q=0, session=0)

        # Check number of tags read
        tag_count = reader.GetTagCount()
        # Get data of read tags
        for idx in range(tag_count):
            tag_data = reader.GetTagData(idx=idx)
        reader.ClearTags()

    # Configure the callback
    reader.set_notification_callback(notification_callback=my_callback)

    # Start inventory stream
    reader.StartInventoryStream(rounds=10, q=0, session=0)

    time.sleep(1)

    # Stop inventory stream
    reader.StopInventoryStream()

    assert tag_data is not None
