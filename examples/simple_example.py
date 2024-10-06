import logging
import time

# To use from source
from src.nurapi import NUR, NurModuleSetup, NUR_MODULESETUP_FLAGS, NurInventoryStreamData
from src.nurapi.enums import SETUP_RX_DEC, SETUP_LINK_FREQ, NurBank

# To use from installed package
# from nurapi import NUR, NurModuleSetup, NUR_MODULESETUP_FLAGS, NurInventoryStreamData
# from nurapi.enums import SETUP_RX_DEC, SETUP_LINK_FREQ, NurBank

logging.basicConfig(level=logging.DEBUG)

## CONNECT
# Create driver
reader = NUR()

# Enable USB autoconnect
#reader.SetUsbAutoConnect(True)

# OR Connect to specific serial port
reader.ConnectSerialPortEx(port_name='COM8')
#reader.ConnectSerialPort(port_numer=8)

# Check connection status just by checking physical layer status
reader.IsConnected()
# Check connection status checking full transport layer
reader.Ping()

## GET INFO
reader_info = reader.GetReaderInfo()

device_caps = reader.GetDeviceCaps()

## MODULE SETUP

# Try a configuration
module_setup = NurModuleSetup()
module_setup.link_freq = SETUP_LINK_FREQ.BLF_160
module_setup.rx_decoding = SETUP_RX_DEC.FM0
desired_tx_level_dbm = 25
module_setup.tx_level = ((device_caps.maxTxdBm - desired_tx_level_dbm) *
                         device_caps.txAttnStep)
module_setup.antenna_mask_ex = 0b00000001  # Antenna 1 (BIT0)
module_setup.selected_antenna = -1  # Automatic selection
reader.SetModuleSetup(
    setup_flags=[
        NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_TXLEVEL,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_ANTMASKEX,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_SELECTEDANT
    ],
    module_setup=module_setup)

module_setup = reader.GetModuleSetup(
    setup_flags=[
        NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_TXLEVEL,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_ANTMASKEX,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_SELECTEDANT
    ])

# Try a different configuration
module_setup.link_freq = SETUP_LINK_FREQ.BLF_160
module_setup.rx_decoding = SETUP_RX_DEC.FM0
reader.SetModuleSetup(
    setup_flags=[
        NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC
    ],
    module_setup=module_setup)

module_setup = reader.GetModuleSetup(
    setup_flags=[
        NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC
    ])

## SIMPLE INVENTORY
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

## INVENTORY STREAM
some_epc: bytearray | None = None


# Define callback
def my_callback(inventory_stream_data: NurInventoryStreamData):
    global some_epc
    # If stream stopped, restart
    if inventory_stream_data.stopped:
        reader.StartInventoryStream(rounds=10, q=0, session=0)

    # Check number of tags read
    tag_count = reader.GetTagCount()
    # Get data of read tags
    for idx in range(tag_count):
        tag_data = reader.GetTagData(idx=idx)
        some_epc = tag_data.epc
    reader.ClearTags()


# Configure the callback
reader.set_notification_callback(notification_callback=my_callback)

# Start inventory stream
reader.StartInventoryStream(rounds=10, q=0, session=0)
time.sleep(1)
# Stop inventory stream
reader.StopInventoryStream()

## READ WRITE OPERATIONS
if some_epc is not None:
    reader.WriteTagByEPC(passwd=0,
                         secured=False,
                         epc=some_epc,
                         bank=NurBank.NUR_BANK_USER,
                         address=0,
                         byte_count=2,
                         data=bytearray([0x12, 0x34]))
    data = reader.ReadTagByEPC(passwd=0,
                               secured=False,
                               epc=some_epc,
                               bank=NurBank.NUR_BANK_USER,
                               address=0,
                               byte_count=2)
    reader.WriteTagByEPC(passwd=0,
                         secured=False,
                         epc=some_epc,
                         bank=NurBank.NUR_BANK_USER,
                         address=0,
                         byte_count=2,
                         data=bytearray([0x56, 0x78]))
    data = reader.ReadTagByEPC(passwd=0,
                               secured=False,
                               epc=some_epc,
                               bank=NurBank.NUR_BANK_USER,
                               address=0,
                               byte_count=2)

# Disconnect reader
reader.Disconnect()
