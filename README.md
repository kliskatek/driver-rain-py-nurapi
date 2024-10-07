# nurapi

[![PyPI - Version](https://img.shields.io/pypi/v/nurapi.svg)](https://pypi.org/project/nurapi)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nurapi.svg)](https://pypi.org/project/nurapi)
![OS](https://img.shields.io/badge/os-windows-blue)
-----
*Python driver for NordicID UHF RFID readers wrapping NurApi*
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Connect to the reader](#connect-to-the-reader)
  - [Get basic information about the reader](#get-basic-information-about-the-reader)
  - [Configure the reader](#configure-the-reader)
  - [Perform single synchronous inventory](#perform-single-synchronous-inventory)
  - [Perform continuous asynchronous inventory](#perform-continuous-asynchronous-inventory)
  - [Execute Read/Write operations](#execute-readwrite-operations)
- [License](#license)

## Installation

```console
pip install nurapi
```

## Usage
### Connect to the reader
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
### Get basic information about the reader
```python
## GET INFO
reader_info = reader.GetReaderInfo()
device_caps = reader.GetDeviceCaps()
```
Sample response values:

`
reader_info = NurReaderInfo(serial='K134500382', alt_serial='K134700326', name='STIX', fcc_id='',  hw_version='PWM0022', sw_ver_major=5, sw_ver_minor=10, dev_build=65, num_gpio=0, num_sensors=0, num_regions=21, num_antennas=1,  max_antennas=1)
`

`
device_caps = NurDeviceCaps(dwSize=40, flagSet1=15696847, flagSet2=0, maxTxdBm=27, txAttnStep=1, maxTxmW=500, txSteps=20, szTagBuffer=630, curCfgMaxAnt=1, curCfgMaxGPIO=0, chipVersion=2, moduleType=3, moduleConfigFlags=4, v2Level=1, secChipMajorVersion=0, secChipMinorVersion=0, secChipMaintenanceVersion=0, secChipReleaseVersion=0)
`


### Configure the reader

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
```
### Perform single synchronous inventory
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
### Perform continuous asynchronous inventory

```python
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

# Do other stuff
time.sleep(1)

# Stop inventory stream
reader.StopInventoryStream()
```
Sample report:

`
NurTagData(timestamp=11, rssi=-51, scaled_rssi=93, freq=866.9, pc=bytearray(b'4\x00'), channel=2, antenna_id=0, epc_len=12, epc=bytearray(b'Q\x10\x12\x03(\x000\x00\x00\x00V\x04'))
`
### Execute Read/Write operations
```python
reader.WriteTagByEPC(
    epc=bytes.fromhex('010203040506070809101112'),
    secured=False, 
    passwd=0, 
    bank=NurBank.NUR_BANK_USER, 
    address=0, 
    byte_count=2, 
    data=bytearray([0x12, 0x34]))

data: bytearray = reader.ReadTagByEPC(
    epc=bytes.fromhex('010203040506070809101112'),
    secured=False, 
    passwd=0, 
    bank=NurBank.NUR_BANK_USER, 
    address=0, 
    byte_count=2)
```

## License

`nurapi` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
