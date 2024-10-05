import ctypes
from importlib.resources import files
import platform

from .structures import _C_NUR_INVENTORY_RESPONSE, _C_NUR_TAG_DATA, _C_NUR_MODULESETUP, _C_NUR_INVENTORYSTREAM_DATA, \
    _C_NUR_READERINFO, _C_NUR_DEVICECAPS


class NurApiBindings:
    _nurapi_dll_path = None

    # Detect Source or Package mode
    top_package = __name__.split('.')[0]
    if top_package == 'src':
        nurapi_package = files('src.nurapi')
    else:
        nurapi_package = files('nurapi')

    if platform.system() == 'Windows':
        if platform.architecture()[0] == '64bit':
            _nurapi_dll_path = nurapi_package.joinpath('lib').joinpath(
                'windows').joinpath('x64').joinpath('NURAPI.dll')
        if platform.architecture()[0] == '32bit':
            _nurapi_dll_path = nurapi_package.joinpath('lib').joinpath(
                'windows').joinpath('x86').joinpath('NURAPI.dll')

    if _nurapi_dll_path is None:
        raise Exception('OS/Platform not supported')
    _nurapi_dll = ctypes.CDLL(_nurapi_dll_path)

    Create = _nurapi_dll.NurApiCreate
    Create.argtypes = []
    Create.restype = ctypes.c_void_p

    SetUsbAutoConnect = _nurapi_dll.NurApiSetUsbAutoConnect
    SetUsbAutoConnect.argtypes = [ctypes.c_void_p, ctypes.c_int]
    SetUsbAutoConnect.restype = ctypes.c_int

    ConnectSerialPort = _nurapi_dll.NurApiConnectSerialPort
    ConnectSerialPort.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    ConnectSerialPort.restype = ctypes.c_int

    ConnectSerialPortEx = _nurapi_dll.NurApiConnectSerialPortEx
    ConnectSerialPortEx.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]
    ConnectSerialPortEx.restype = ctypes.c_int

    ClearTags = _nurapi_dll.NurApiClearTags
    ClearTags.argtypes = [ctypes.c_void_p]
    ClearTags.restype = ctypes.c_int

    SimpleInventory = _nurapi_dll.NurApiSimpleInventory
    SimpleInventory.argtypes = [ctypes.c_void_p, ctypes.POINTER(_C_NUR_INVENTORY_RESPONSE)]
    SimpleInventory.restype = ctypes.c_int

    FetchTags = _nurapi_dll.NurApiFetchTags
    FetchTags.argtypes = [ctypes.c_void_p, ctypes.c_bool, ctypes.POINTER(ctypes.c_int)]
    FetchTags.restype = ctypes.c_int

    GetTagCount = _nurapi_dll.NurApiGetTagCount
    GetTagCount.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
    GetTagCount.restype = ctypes.c_int

    GetTagData = _nurapi_dll.NurApiGetTagData
    GetTagData.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(_C_NUR_TAG_DATA)]
    GetTagData.restype = ctypes.c_int

    StartInventoryStream = _nurapi_dll.NurApiStartInventoryStream
    StartInventoryStream.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    StartInventoryStream.restype = ctypes.c_int

    StopInventoryStream = _nurapi_dll.NurApiStopInventoryStream
    StopInventoryStream.argtypes = [ctypes.c_void_p]
    StopInventoryStream.restype = ctypes.c_int

    SetNotificationCallback = _nurapi_dll.NurApiSetNotificationCallback
    SetNotificationCallback.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    SetNotificationCallback.restype = ctypes.c_int

    SetModuleSetup = _nurapi_dll.NurApiSetModuleSetup
    SetModuleSetup.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(_C_NUR_MODULESETUP),
                               ctypes.c_ulong]
    SetModuleSetup.restype = ctypes.c_int

    GetModuleSetup = _nurapi_dll.NurApiGetModuleSetup
    GetModuleSetup.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(_C_NUR_MODULESETUP),
                               ctypes.c_ulong]
    GetModuleSetup.restype = ctypes.c_int

    IsConnected = _nurapi_dll.NurApiIsConnected
    IsConnected.argtypes = [ctypes.c_void_p]
    IsConnected.restype = ctypes.c_int

    Ping = _nurapi_dll.NurApiPing
    Ping.argtypes = [ctypes.c_void_p]
    Ping.restype = ctypes.c_int

    Disconnect = _nurapi_dll.NurApiDisconnect
    Disconnect.argtypes = [ctypes.c_void_p]
    Disconnect.restype = ctypes.c_int

    GetReaderInfo = _nurapi_dll.NurApiGetReaderInfo
    GetReaderInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(_C_NUR_READERINFO),
                              ctypes.c_ulong]
    GetReaderInfo.restype = ctypes.c_int

    GetDeviceCaps = _nurapi_dll.NurApiGetDeviceCaps
    GetDeviceCaps.argtypes = [ctypes.c_void_p, ctypes.POINTER(_C_NUR_DEVICECAPS),
                              ctypes.c_ulong]
    GetDeviceCaps.restype = ctypes.c_int

    ReadTagByEPC = _nurapi_dll.NurApiReadTagByEPC
    ReadTagByEPC.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_bool, ctypes.c_char_p,
                             ctypes.c_ulong, ctypes.c_byte, ctypes.c_ulong, ctypes.c_int, ctypes.c_char_p]
    ReadTagByEPC.restype = ctypes.c_int

    WriteTagByEPC = _nurapi_dll.NurApiWriteTagByEPC
    WriteTagByEPC.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_bool, ctypes.c_char_p,
                              ctypes.c_ulong, ctypes.c_byte, ctypes.c_ulong, ctypes.c_int, ctypes.c_char_p]
    WriteTagByEPC.restype = ctypes.c_int
