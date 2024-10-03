import ctypes
import inspect
import logging
from typing import List

from _ctypes import byref
from rain_readers.nur import NUR_MODULESETUP

from .bindings import NurApiBindings
from .enums import NUR_NOTIFICATION, NUR_MODULESETUP_FLAGS, OperationResult
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
                inventory_stream_data = NurInventoryStreamData(
                    c_object=ctypes.cast(data, ctypes.POINTER(_C_NUR_INVENTORYSTREAM_DATA)).contents)
                if self._user_inventory_notification_callback is not None:
                    self._user_inventory_notification_callback(inventory_stream_data)

        self.ctype_callback = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_ulong, ctypes.c_int,
                                               ctypes.c_void_p,
                                               ctypes.c_int)(CNotificationCallback)
        self._SetNotificationCallback(self.ctype_callback)

    @staticmethod
    def _log_op_result(op_name: str, c_res: int):
        op_res = OperationResult(c_res == 0)
        logging.debug('NurApi.' + str(op_name) + ': ' + str(op_res))
        return op_res

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
        return NUR._log_op_result(op_name='SetUsbAutoConnect(' + str(enable) + ')', c_res=res)

    def IsConnected(self):
        res = NurApiBindings.IsConnected(self._h_api)
        return NUR._log_op_result(op_name='IsConnected', c_res=res)

    def Disconnect(self):
        res = NurApiBindings.Disconnect(self._h_api)
        return NUR._log_op_result(op_name='Disconnect', c_res=res)

    def Ping(self):
        res = NurApiBindings.Ping(self._h_api)
        return NUR._log_op_result(op_name='Ping', c_res=res)

    def ClearTags(self):
        res = NurApiBindings.ClearTags(self._h_api)
        return NUR._log_op_result(op_name='ClearTags', c_res=res)

    def SimpleInventory(self, inventory_response: NurInventoryResponse):
        c_inventory_response = _C_NUR_INVENTORY_RESPONSE()
        res = NurApiBindings.SimpleInventory(self._h_api, byref(c_inventory_response))
        inventory_response.from_Ctype(c_inventory_response)
        logger.debug(inventory_response)
        return NUR._log_op_result(op_name='SimpleInventory', c_res=res)

    def FetchTags(self, includeMeta, tag_count: NurTagCount):
        tags = ctypes.c_int()
        res = NurApiBindings.FetchTags(self._h_api, includeMeta, byref(tags))
        tag_count.count = tags.value
        logger.debug(tag_count)
        return NUR._log_op_result(op_name='FetchTags', c_res=res)

    def GetTagCount(self, tag_count: NurTagCount):
        c_count = ctypes.c_int()
        res = NurApiBindings.GetTagCount(self._h_api, byref(c_count))
        tag_count.count = c_count.value
        logger.debug(tag_count)
        return NUR._log_op_result(op_name='GetTagCount', c_res=res)

    def GetTagData(self, idx, tag_data: NurTagData):
        c_tag_data = _C_NUR_TAG_DATA()
        res = NurApiBindings.GetTagData(self._h_api, idx, byref(c_tag_data))
        tag_data.from_Ctype(c_tag_data)
        logger.debug(tag_data)
        return NUR._log_op_result(op_name='GetTagData', c_res=res)

    def StartInventoryStream(self, rounds: int, q: int, session: int):
        c_rounds = ctypes.c_int(rounds)
        c_q = ctypes.c_int(q)
        c_session = ctypes.c_int(session)
        res = NurApiBindings.StartInventoryStream(self._h_api, c_rounds, c_q, c_session)
        return NUR._log_op_result(op_name='StartInventoryStream', c_res=res)

    def StopInventoryStream(self):
        res = NurApiBindings.StopInventoryStream(self._h_api)
        return NUR._log_op_result(op_name='StopInventoryStream', c_res=res)

    def _SetNotificationCallback(self, c_notification_callback):
        res = NurApiBindings.SetNotificationCallback(self._h_api, c_notification_callback)
        return NUR._log_op_result(op_name='SetNotificationCallback', c_res=res)

    def SetModuleSetup(self, setupFlags: List[NUR_MODULESETUP_FLAGS], module_setup: NurModuleSetup):
        c_module_setup = _C_NUR_MODULESETUP(py_object=module_setup)
        combinde_flags = 0
        for setupFlag in setupFlags:
            combinde_flags += setupFlag.value
        c_setupflags = ctypes.c_ulong(combinde_flags)
        res = NurApiBindings.SetModuleSetup(self._h_api, c_setupflags, byref(c_module_setup),
                                            ctypes.sizeof(c_module_setup))
        return NUR._log_op_result(op_name='SetModuleSetup', c_res=res)

    def GetModuleSetup(self, setupFlags: List[NUR_MODULESETUP_FLAGS], module_setup: NurModuleSetup):
        c_module_setup = _C_NUR_MODULESETUP()
        combinde_flags = 0
        for setupFlag in setupFlags:
            combinde_flags += setupFlag.value
        c_setupflags = ctypes.c_ulong(combinde_flags)
        res = NurApiBindings.GetModuleSetup(self._h_api, c_setupflags, byref(c_module_setup),
                                            ctypes.sizeof(c_module_setup))
        module_setup.from_Ctype(c_object=c_module_setup)
        logger.debug(module_setup)
        return NUR._log_op_result(op_name='GetModuleSetup', c_res=res)

    def GetReaderInfo(self, reader_info: NurReaderInfo):
        c_readerinfo = _C_NUR_READERINFO()
        res = NurApiBindings.GetReaderInfo(self._h_api, byref(c_readerinfo), ctypes.sizeof(c_readerinfo))
        reader_info.from_Ctype(c_object=c_readerinfo)
        logger.debug(reader_info)
        return NUR._log_op_result(op_name='GetReaderInfo', c_res=res)

    def GetDeviceCaps(self, device_caps: NurDeviceCaps):
        c_device_caps = _C_NUR_DEVICECAPS()
        res = NurApiBindings.GetDeviceCaps(self._h_api, byref(c_device_caps), ctypes.sizeof(c_device_caps))
        device_caps.from_Ctype(c_object=c_device_caps)
        logger.debug(device_caps)
        return NUR._log_op_result(op_name='GetDeviceCaps', c_res=res)
