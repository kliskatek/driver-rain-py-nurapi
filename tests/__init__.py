# Create driver
from src.nurapi import NUR

reader = NUR()
reader.ConnectSerialPortEx(port_name='COM8')