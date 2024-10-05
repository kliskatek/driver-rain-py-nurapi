import ctypes
import logging
from typing import List

from _ctypes import byref

from .bindings import NurApiBindings
from .enums import NUR_NOTIFICATION, NUR_MODULESETUP_FLAGS, OperationResult, NurBank
from .helpers import create_c_byte_buffer, create_c_wchar_buffer
from .structures import _C_NUR_INVENTORY_RESPONSE, _C_NUR_TAG_DATA, _C_NUR_MODULESETUP, _C_NUR_INVENTORYSTREAM_DATA, \
    NurTagCount, NurTagData, NurInventoryStreamData, NurInventoryResponse, NurModuleSetup, _C_NUR_READERINFO, \
    NurReaderInfo, NurDeviceCaps, _C_NUR_DEVICECAPS

logger = logging.getLogger(__name__)


class NUR:

    def __init__(self):
        self._h_api = None
        self._Create()
        self._user_inventory_notification_callback = None

        def CNotificationCallback(h_api, timestamp, type, data, dataLen):
            logging.debug('NurApi.Notification: ' + str(NUR_NOTIFICATION(type)))
            if NUR_NOTIFICATION(type) == NUR_NOTIFICATION.NUR_NOTIFICATION_INVENTORYSTREAM:
                inventory_stream_data = NurInventoryStreamData()
                inventory_stream_data.from_Ctype(
                    c_object=ctypes.cast(data, ctypes.POINTER(_C_NUR_INVENTORYSTREAM_DATA)).contents)
                if self._user_inventory_notification_callback is not None:
                    self._user_inventory_notification_callback(inventory_stream_data)

        self.ctype_callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_ulong, ctypes.c_int,
                                               ctypes.c_void_p,
                                               ctypes.c_int)(CNotificationCallback)
        self._SetNotificationCallback(self.ctype_callback)

    @staticmethod
    def _check_op_result(op_name: str, c_res: int):
        op_res = OperationResult(c_res == 0)
        logging.debug('NurApi.' + str(op_name) + ': ' + str(op_res))
        if op_res != OperationResult.SUCCESS:
            raise Exception('Operation result for ' + op_name + ': ' + op_res.name)
        return True

    def _Create(self):
        h_api = NurApiBindings.Create()
        if h_api == -1:
            logger.error('NurApi.Create failed')
            return False
        self._h_api = h_api
        logging.debug('NurApi.Create succeeded with API handler: ' + str(h_api))
        return True

    def set_user_inventory_notification_callback(self, inventory_notification_callback):
        self._user_inventory_notification_callback = inventory_notification_callback

    def SetUsbAutoConnect(self, enable):
        res = NurApiBindings.SetUsbAutoConnect(self._h_api, enable)
        NUR._check_op_result(op_name='SetUsbAutoConnect(' + str(enable) + ')', c_res=res)

    def IsConnected(self):
        res = NurApiBindings.IsConnected(self._h_api)
        try:
            NUR._check_op_result(op_name='IsConnected', c_res=res)
            return True
        except Exception:
            return False

    def Disconnect(self):
        res = NurApiBindings.Disconnect(self._h_api)
        NUR._check_op_result(op_name='Disconnect', c_res=res)

    def Ping(self):
        res = NurApiBindings.Ping(self._h_api)
        try:
            NUR._check_op_result(op_name='Ping', c_res=res)
            return True
        except Exception:
            return False

    def ClearTags(self):
        res = NurApiBindings.ClearTags(self._h_api)
        NUR._check_op_result(op_name='ClearTags', c_res=res)

    def SimpleInventory(self):
        c_inventory_response = _C_NUR_INVENTORY_RESPONSE()
        res = NurApiBindings.SimpleInventory(self._h_api, byref(c_inventory_response))
        NUR._check_op_result(op_name='SimpleInventory', c_res=res)
        inventory_response = NurInventoryResponse()
        inventory_response.from_Ctype(c_inventory_response)
        logger.debug(inventory_response)
        return inventory_response

    def FetchTags(self, include_meta: bool = True):
        c_tags = ctypes.c_int()
        c_include_meta = ctypes.c_bool(include_meta)
        res = NurApiBindings.FetchTags(self._h_api, c_include_meta, byref(c_tags))
        NUR._check_op_result(op_name='FetchTags', c_res=res)
        tags = c_tags.value
        logger.debug('Fetched tags: ' + str(tags))
        return tags

    def GetTagCount(self):
        c_count = ctypes.c_int()
        res = NurApiBindings.GetTagCount(self._h_api, byref(c_count))
        NUR._check_op_result(op_name='GetTagCount', c_res=res)
        tag_count = c_count.value
        logger.debug('Tag count: ' + str(tag_count))
        return tag_count

    def GetTagData(self, idx):
        c_tag_data = _C_NUR_TAG_DATA()
        res = NurApiBindings.GetTagData(self._h_api, idx, byref(c_tag_data))
        NUR._check_op_result(op_name='GetTagData', c_res=res)
        tag_data = NurTagData()
        tag_data.from_Ctype(c_tag_data)
        logger.debug(tag_data)
        return tag_data

    def StartInventoryStream(self, rounds: int, q: int, session: int):
        c_rounds = ctypes.c_int(rounds)
        c_q = ctypes.c_int(q)
        c_session = ctypes.c_int(session)
        res = NurApiBindings.StartInventoryStream(self._h_api, c_rounds, c_q, c_session)
        NUR._check_op_result(op_name='StartInventoryStream', c_res=res)

    def StopInventoryStream(self):
        res = NurApiBindings.StopInventoryStream(self._h_api)
        NUR._check_op_result(op_name='StopInventoryStream', c_res=res)

    def _SetNotificationCallback(self, c_notification_callback):
        res = NurApiBindings.SetNotificationCallback(self._h_api, c_notification_callback)
        NUR._check_op_result(op_name='SetNotificationCallback', c_res=res)

    def SetModuleSetup(self, setupFlags: List[NUR_MODULESETUP_FLAGS], module_setup: NurModuleSetup):
        c_module_setup = _C_NUR_MODULESETUP(py_object=module_setup)
        combinde_flags = 0
        for setupFlag in setupFlags:
            combinde_flags += setupFlag.value
        c_setupflags = ctypes.c_ulong(combinde_flags)
        res = NurApiBindings.SetModuleSetup(self._h_api, c_setupflags, byref(c_module_setup),
                                            ctypes.sizeof(c_module_setup))
        NUR._check_op_result(op_name='SetModuleSetup', c_res=res)
        logger.debug('Set: ' + str(module_setup))

    def GetModuleSetup(self, setupFlags: List[NUR_MODULESETUP_FLAGS]):
        c_module_setup = _C_NUR_MODULESETUP()
        combinde_flags = 0
        for setupFlag in setupFlags:
            combinde_flags += setupFlag.value
        c_setupflags = ctypes.c_ulong(combinde_flags)
        res = NurApiBindings.GetModuleSetup(self._h_api, c_setupflags, byref(c_module_setup),
                                            ctypes.sizeof(c_module_setup))
        NUR._check_op_result(op_name='GetModuleSetup', c_res=res)
        module_setup = NurModuleSetup()
        module_setup.from_Ctype(c_object=c_module_setup)
        logger.debug('Get: ' + str(module_setup))
        return module_setup

    def GetReaderInfo(self):
        c_readerinfo = _C_NUR_READERINFO()
        res = NurApiBindings.GetReaderInfo(self._h_api, byref(c_readerinfo), ctypes.sizeof(c_readerinfo))
        NUR._check_op_result(op_name='GetReaderInfo', c_res=res)
        reader_info = NurReaderInfo()
        reader_info.from_Ctype(c_object=c_readerinfo)
        logger.debug(reader_info)
        return reader_info

    def GetDeviceCaps(self):
        c_device_caps = _C_NUR_DEVICECAPS()
        res = NurApiBindings.GetDeviceCaps(self._h_api, byref(c_device_caps), ctypes.sizeof(c_device_caps))
        NUR._check_op_result(op_name='GetDeviceCaps', c_res=res)
        device_caps = NurDeviceCaps()
        device_caps.from_Ctype(c_object=c_device_caps)
        logger.debug(device_caps)
        return device_caps

    def ReadTagByEPC(self, passwd: int, secured: bool, epc: bytearray, bank: NurBank,
                     address: int, byte_count: int):
        c_passwd = ctypes.c_ulong(passwd)
        c_secured = ctypes.c_bool(secured)
        c_epc_buffer = ctypes.create_string_buffer(init=bytes(epc), size=len(epc))
        c_epc_buffer_len = ctypes.c_ulong(len(epc))
        c_bank = ctypes.c_byte(bank.value)
        c_address = ctypes.c_ulong(address)
        c_byte_count = ctypes.c_int(byte_count)
        c_data = ctypes.create_string_buffer(byte_count)
        res = NurApiBindings.ReadTagByEPC(self._h_api, c_passwd, c_secured, c_epc_buffer, c_epc_buffer_len,
                                          c_bank, c_address, c_byte_count, c_data)
        try:
            NUR._check_op_result(op_name='ReadTagByEPC', c_res=res)
            data = bytearray(c_data.value)
            logger.debug('Read: 0x' + str(data.hex()) + '@' + bank.name + '.' + str(address))
            return data
        except Exception as e:
            logger.warning(e)
            return None

    def WriteTagByEPC(self, passwd: int, secured: bool, epc: bytearray, bank: NurBank,
                      address: int, byte_count: int, data: bytearray):
        c_passwd = ctypes.c_ulong(passwd)
        c_secured = ctypes.c_bool(secured)
        c_epc_buffer = ctypes.create_string_buffer(init=bytes(epc), size=len(epc))
        c_epc_buffer_len = ctypes.c_ulong(len(epc))
        c_bank = ctypes.c_byte(bank.value)
        c_address = ctypes.c_ulong(address)
        c_byte_count = ctypes.c_int(byte_count)
        c_data = ctypes.create_string_buffer(init=bytes(data), size=len(data))
        res = NurApiBindings.WriteTagByEPC(self._h_api, c_passwd, c_secured, c_epc_buffer, c_epc_buffer_len,
                                           c_bank, c_address, c_byte_count, c_data)
        try:
            NUR._check_op_result(op_name='WriteTagByEPC', c_res=res)
            logger.debug('Write: 0x' + str(data.hex()) + '@' + bank.name + '.' + str(address))
            return True
        except Exception as e:
            logger.warning(e)
            return False

    def ConnectSerialPort(self, port_numer: int, baud_rate: int = 115200):
        c_port_numer = ctypes.c_int(port_numer)
        c_baud_rate = ctypes.c_int(baud_rate)
        res = NurApiBindings.ConnectSerialPort(self._h_api, c_port_numer, c_baud_rate)
        NUR._check_op_result(op_name='ConnectSerialPort', c_res=res)

    def ConnectSerialPortEx(self, port_name: str, baud_rate: int = 115200):
        c_port_name = create_c_wchar_buffer(port_name)
        c_baud_rate = ctypes.c_int(baud_rate)
        res = NurApiBindings.ConnectSerialPortEx(self._h_api, c_port_name, c_baud_rate)
        NUR._check_op_result(op_name='ConnectSerialPortEx', c_res=res)
