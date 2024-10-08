import ctypes
import platform


def create_c_wchar_buffer(text: str):
    # Handle differences for wchar in Windows/Linux
    buf = None
    if platform.system() == 'Windows':
        buftype = ctypes.c_wchar * (len(text) + 1)
        buf = buftype()
        buf.value = text
        return buf
    elif platform.system() == 'Linux':
        # Linux string
        buftype = ctypes.c_char * (len(text) + 1)
        buf = buftype()
        buf.value = bytes(text, 'utf-8')

        return ctypes.cast(buf, ctypes.c_wchar_p)
