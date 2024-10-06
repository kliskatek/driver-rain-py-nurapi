# nurapi

[![PyPI - Version](https://img.shields.io/pypi/v/nurapi.svg)](https://pypi.org/project/nurapi)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nurapi.svg)](https://pypi.org/project/nurapi)
![OS](https://img.shields.io/badge/os-windows-blue)
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install nurapi
```

## Usage
Connect to the reader:
```python
# Create driver
reader = NUR()

# Connect
reader.ConnectSerialPortEx(port_name='COM8')
# or reader.ConnectSerialPort(port_numer=8)
# or reader.SetUsbAutoConnect(True)

# Check connection status just by checking physical layer status
reader.IsConnected()
# Check connection status checking full transport layer
reader.Ping()

... use the reader ...

# Disconnect reader
reader.Disconnect()
```
Get basic information about the reader:
```python
## GET INFO
reader_info = reader.GetReaderInfo()
device_caps = reader.GetDeviceCaps()
```
Configure the reader:
```python
## MODULE SETUP
module_setup = NurModuleSetup()
module_setup.link_freq = SETUP_LINK_FREQ.BLF_160
module_setup.rx_decoding = SETUP_RX_DEC.FM0
desired_tx_level_dbm = 25
module_setup.tx_level = ((device_caps.maxTxdBm - desired_tx_level_dbm) * 
                         device_caps.txAttnStep)
module_setup.antenna_mask_ex = 0b00000001  # Antenna 1 (BIT0)
module_setup.selected_antenna = -1  # Automatic selection
reader.SetModuleSetup(
    setupFlags=[
        NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_TXLEVEL,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_ANTMASKEX,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_SELECTEDANT
    ],
    module_setup=module_setup)

module_setup = reader.GetModuleSetup(
    setupFlags=[
        NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_TXLEVEL,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_ANTMASKEX,
        NUR_MODULESETUP_FLAGS.NUR_SETUP_SELECTEDANT
    ])```
Perform single synchronous inventory:
```python
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
```
Perform continuous asynchronous inventory:
```python
# Define callback
def callback(inventory_stream_data):
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
reader.set_user_inventory_notification_callback(inventory_notification_callback=callback)

# Start inventory stream
reader.StartInventoryStream(rounds=10, q=0, session=0)

# Do other stuff
time.sleep(1)

# Stop inventory stream
reader.StopInventoryStream()
```
Execute Read/Write operations:
```python
reader.WriteTagByEPC(epc=bytes.fromhex('010203040506070809101112'),
                     secured=False, 
                     passwd=0, 
                     bank=NurBank.NUR_BANK_USER, 
                     address=0, 
                     byte_count=2, 
                     data=bytearray([0x12, 0x34]))

data = reader.ReadTagByEPC(epc=bytes.fromhex('010203040506070809101112'),
                           secured=False, 
                           passwd=0, 
                           bank=NurBank.NUR_BANK_USER, 
                           address=0, 
                           byte_count=2)
```

## License

`nurapi` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
