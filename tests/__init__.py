# Create driver
from src.nurapi import NUR, NurDeviceCaps, NurReaderInfo

reader_port_name = 'COM8'
present_tag_epc = bytearray(b'Q\x10\x12\x03(\x000\x00\x00\x00V\x04')

reader = NUR()