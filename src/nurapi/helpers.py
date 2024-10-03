import ctypes


def create_c_byte_buffer(data: bytearray):
    buftype = ctypes.c_byte * len(data)
    buf = buftype()
    buf.value = bytes(data)
    return buf