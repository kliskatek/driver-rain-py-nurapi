import ctypes


def create_c_byte_buffer(data: bytearray):
    buftype = ctypes.c_byte * len(data)
    buf = buftype()
    buf.value = bytes(data)
    return buf
def create_c_wchar_buffer(text: str):
    buftype = ctypes.c_wchar * (len(text)+1)
    buf = buftype()
    buf.value = text
    return buf