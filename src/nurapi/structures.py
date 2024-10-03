import ctypes
import struct
from dataclasses import dataclass
from enum import Enum
from typing import List

from dataclasses_json import dataclass_json

from .enums import SETUP_RX_DEC, SETUP_LINK_FREQ


class _C_NUR_INVENTORY_RESPONSE(ctypes.Structure):
    _fields_ = [('numTagsFound', ctypes.c_int),
                ('numTagsMem', ctypes.c_int),
                ('roundsDone', ctypes.c_int),
                ('collisions', ctypes.c_int),
                ('Q', ctypes.c_int)]


@dataclass_json
@dataclass
class NurInventoryResponse:
    num_tags_found: int = None
    num_tags_mem: int = None
    rounds_done: int = None
    collisions: int = None
    Q: int = None

    def from_Ctype(self, c_object: _C_NUR_INVENTORY_RESPONSE):
        self.num_tags_found = c_object.numTagsFound
        self.num_tags_mem = c_object.numTagsMem
        self.rounds_done = c_object.roundsDone
        self.collisions = c_object.collisions
        self.Q = c_object.Q


@dataclass_json
@dataclass
class NurTagCount:
    count: int = None


class _C_NUR_TAG_DATA(ctypes.Structure):
    _fields_ = [('timestamp', ctypes.c_ushort),
                ('rssi', ctypes.c_byte),
                ('scaledRssi', ctypes.c_ubyte),
                ('freq', ctypes.c_ulong),
                ('pc', ctypes.c_ushort),
                ('channel', ctypes.c_byte),
                ('antennaId', ctypes.c_byte),
                ('epcLen', ctypes.c_byte),
                ('epc', ctypes.c_ubyte * 62)]


@dataclass_json
@dataclass
class NurTagData:
    timestamp: int = None
    rssi: int = None
    scaled_rssi: int = None
    freq: float = None
    pc: bytearray = None
    channel: int = None
    antenna_id: int = None
    epc_len: int = None
    epc: bytearray = None

    def from_Ctype(self, c_object: _C_NUR_TAG_DATA):
        self.timestamp: int = c_object.timestamp
        self.rssi = c_object.rssi
        self.scaled_rssi = c_object.scaledRssi
        self.freq = c_object.freq / 1000
        self.pc = bytearray(struct.pack('>H', c_object.pc))
        self.channel = c_object.channel
        self.antenna_id = c_object.antennaId
        self.epc_len = c_object.epcLen
        self.epc = bytearray(c_object.epc[:c_object.epcLen])


class _C_NUR_RSSI_FILTER(ctypes.Structure):
    _fields_ = [('min', ctypes.c_char),
                ('max', ctypes.c_char)]


class _C_NUR_AUTOTUNE_SETUP(ctypes.Structure):
    _fields_ = [('mode', ctypes.c_byte),
                ('threshold_dBm', ctypes.c_char)]


class _C_NUR_MODULESETUP(ctypes.Structure):
    _fields_ = [('linkFreq', ctypes.c_int),
                ('rxDecoding', ctypes.c_int),
                ('txLevel', ctypes.c_int),
                ('txModulation', ctypes.c_int),
                ('regionId', ctypes.c_int),
                ('inventoryQ', ctypes.c_int),
                ('inventorySession', ctypes.c_int),
                ('inventoryRounds', ctypes.c_int),
                ('antennaMask', ctypes.c_int),
                ('scanSingleTriggerTimeout', ctypes.c_int),
                ('inventoryTriggerTimeout', ctypes.c_int),
                ('selectedAntenna', ctypes.c_int),
                ('opFlags', ctypes.c_ulong),
                ('inventoryTarget', ctypes.c_int),
                ('inventoryEpcLength', ctypes.c_int),
                ('readRssiFilter', _C_NUR_RSSI_FILTER),
                ('writeRssiFilter', _C_NUR_RSSI_FILTER),
                ('inventoryRssiFilter', _C_NUR_RSSI_FILTER),
                ('readTO', ctypes.c_int),
                ('writeTO', ctypes.c_int),
                ('lockTO', ctypes.c_int),
                ('killTO', ctypes.c_int),
                ('periodSetup', ctypes.c_int),
                ('antPower', ctypes.c_int * 4),
                ('powerOffset', ctypes.c_int * 4),
                ('antennaMaskEx', ctypes.c_ulong),
                ('autotune', _C_NUR_AUTOTUNE_SETUP),
                ('antPowerEx', ctypes.c_int * 32),
                ('rxSensitivity', ctypes.c_int),
                ('rfProfile', ctypes.c_int),
                ('toSleepTime', ctypes.c_int)]

    def __init__(self, py_object=None):
        super().__init__()
        if py_object is not None:
            self.from_py_type(py_object=py_object)

    def from_py_type(self, py_object):
        if issubclass(type(py_object.link_freq), Enum):
            self.linkFreq = py_object.link_freq.value
        else:
            self.linkFreq = py_object.link_freq
        if issubclass(type(py_object.rx_decoding), Enum):
            self.rxDecoding = py_object.rx_decoding.value
        else:
            self.rxDecoding = py_object.rx_decoding
        self.txLevel = py_object.tx_level
        self.txModulation = py_object.tx_modulation
        self.regionId = py_object.region_id
        self.inventoryQ = py_object.inventory_q
        self.inventorySession = py_object.inventory_session
        self.inventoryRounds = py_object.inventory_rounds
        self.antennaMask = py_object.antenna_mask
        self.scanSingleTriggerTimeout = py_object.scan_single_trigger_timeout
        self.inventoryTriggerTimeout = py_object.inventory_trigger_timeout
        self.selectedAntenna = py_object.selected_antenna
        self.opFlags = py_object.op_flags
        self.inventoryTarget = py_object.inventory_target
        self.inventoryEpcLength = py_object.inventory_epc_length
        self.readRssiFilter = py_object.read_rssi_filter
        self.writeRssiFilter = py_object.write_rssi_filter
        self.inventoryRssiFilter = py_object.inventory_rssi_filter
        self.readTO = py_object.read_to
        self.writeTO = py_object.write_to
        self.lockTO = py_object.lock_to
        self.killTO = py_object.kill_to
        self.periodSetup = py_object.period_setup
        self.antPower = py_object.ant_power
        self.powerOffset = py_object.power_offset
        self.antennaMaskEx = py_object.antenna_mask_ex
        self.autotune = py_object.autotune
        self.antPowerEx = py_object.ant_power_ex
        self.rxSensitivity = py_object.rx_sensitivity
        self.rfProfile = py_object.rf_profile
        self.toSleepTime = py_object.to_sleep_time


@dataclass_json
@dataclass
class NurModuleSetup:
    link_freq: SETUP_LINK_FREQ = None
    rx_decoding: SETUP_RX_DEC = None
    tx_level: int = None
    tx_modulation: int = None
    region_id: int = None
    inventory_q: int = None
    inventory_session: int = None
    inventory_rounds: int = None
    antenna_mask: int = None
    scan_single_trigger_timeout: int = None
    inventory_trigger_timeout: int = None
    selected_antenna: int = None
    op_flags: int = None
    inventory_target: int = None
    inventory_epc_length: int = None
    read_rssi_filter: _C_NUR_RSSI_FILTER = None
    write_rssi_filter: _C_NUR_RSSI_FILTER = None
    inventory_rssi_filter: _C_NUR_RSSI_FILTER = None
    read_to: int = None
    write_to: int = None
    lock_to: int = None
    kill_to: int = None
    period_setup: int = None
    ant_power: List[int] = None
    power_offset: List[int] = None
    antenna_mask_ex: int = None
    autotune: _C_NUR_AUTOTUNE_SETUP = None
    ant_power_ex: List[int] = None
    rx_sensitivity: int = None
    rf_profile: int = None
    to_sleep_time: int = None

    def __init__(self, c_object: _C_NUR_MODULESETUP = None):
        super().__init__()
        if c_object is not None:
            self.from_Ctype(c_object)

    def from_Ctype(self, c_object: _C_NUR_MODULESETUP):
        self.link_freq = SETUP_LINK_FREQ(c_object.linkFreq)
        self.rx_decoding = SETUP_RX_DEC(c_object.rxDecoding)
        self.tx_level = c_object.txLevel
        self.tx_modulation = c_object.txModulation
        self.region_id = c_object.regionId
        self.inventory_q = c_object.inventoryQ
        self.inventory_session = c_object.inventorySession
        self.inventory_rounds = c_object.inventoryRounds
        self.antenna_mask = c_object.antennaMask
        self.scan_single_trigger_timeout = c_object.scanSingleTriggerTimeout
        self.inventory_trigger_timeout = c_object.inventoryTriggerTimeout
        self.selected_antenna = c_object.selectedAntenna
        self.op_flags = c_object.opFlags
        self.inventory_target = c_object.inventoryTarget
        self.inventory_epc_length = c_object.inventoryEpcLength
        self.read_rssi_filter = c_object.readRssiFilter
        self.write_rssi_filter = c_object.writeRssiFilter
        self.inventory_rssi_filter = c_object.inventoryRssiFilter
        self.read_to = c_object.readTO
        self.write_to = c_object.writeTO
        self.lock_to = c_object.lockTO
        self.kill_to = c_object.killTO
        self.period_setup = c_object.periodSetup
        self.ant_power = c_object.antPower
        self.power_offset = c_object.powerOffset
        self.antenna_mask_ex = c_object.antennaMaskEx
        self.autotune = c_object.autotune
        self.ant_power_ex = c_object.antPowerEx
        self.rx_sensitivity = c_object.rxSensitivity
        self.rf_profile = c_object.rfProfile
        self.to_sleep_time = c_object.toSleepTime


class _C_NUR_READERINFO(ctypes.Structure):
    _fields_ = [('serial', ctypes.c_wchar * 32),
                ('altSerial', ctypes.c_wchar * 32),
                ('name', ctypes.c_wchar * 32),
                ('fccId', ctypes.c_wchar * 48),
                ('hwVersion', ctypes.c_wchar * 16),
                ('swVerMajor', ctypes.c_int),
                ('swVerMinor', ctypes.c_int),
                ('devBuild', ctypes.c_byte),
                ('numGpio', ctypes.c_int),
                ('numSensors', ctypes.c_int),
                ('numRegions', ctypes.c_int),
                ('numAntennas', ctypes.c_int),
                ('maxAntennas', ctypes.c_int)]


@dataclass_json
@dataclass
class NurReaderInfo:
    serial: str = None
    alt_serial: str = None
    name: str = None
    fcc_id: str = None
    hw_version: str = None
    sw_ver_major: int = None
    sw_ver_minor: int = None
    dev_build: int = None
    num_gpio: int = None
    num_sensors: int = None
    num_regions: int = None
    num_antennas: int = None
    max_antennas: int = None

    def __init__(self, c_object: _C_NUR_READERINFO = None):
        super().__init__()
        if c_object is not None:
            self.from_Ctype(c_object)

    def from_Ctype(self, c_object: _C_NUR_READERINFO):
        self.serial = c_object.serial
        self.alt_serial = c_object.altSerial
        self.name = c_object.name
        self.fcc_id = c_object.fccId
        self.hw_version = c_object.hwVersion
        self.sw_ver_major = c_object.swVerMajor
        self.sw_ver_minor = c_object.swVerMinor
        self.dev_build = c_object.devBuild
        self.num_gpio = c_object.numGpio
        self.num_sensors = c_object.numSensors
        self.num_regions = c_object.numRegions
        self.num_antennas = c_object.numAntennas
        self.max_antennas = c_object.maxAntennas


class _C_NUR_DEVICECAPS(ctypes.Structure):
    _fields_ = [('dwSize', ctypes.c_ulong),
                ('flagSet1', ctypes.c_ulong),
                ('flagSet2', ctypes.c_ulong),
                ('maxTxdBm', ctypes.c_int),
                ('txAttnStep', ctypes.c_int),
                ('maxTxmW', ctypes.c_ushort),
                ('txSteps', ctypes.c_ushort),
                ('szTagBuffer', ctypes.c_ushort),
                ('curCfgMaxAnt', ctypes.c_ushort),
                ('curCfgMaxGPIO', ctypes.c_ushort),
                ('chipVersion', ctypes.c_ushort),
                ('moduleType', ctypes.c_ushort),
                ('moduleConfigFlags', ctypes.c_ulong),
                ('v2Level', ctypes.c_ushort),
                ('secChipMajorVersion', ctypes.c_ulong),
                ('secChipMinorVersion', ctypes.c_ulong),
                ('secChipMaintenanceVersion', ctypes.c_ulong),
                ('secChipReleaseVersion', ctypes.c_ulong),
                ('res', ctypes.c_byte * (128
                                         - 8 * ctypes.sizeof(ctypes.c_ulong)
                                         - 2 * ctypes.sizeof(ctypes.c_int)
                                         - 8 * ctypes.sizeof(ctypes.c_ushort)))]


@dataclass_json
@dataclass
class NurDeviceCaps:
    dwSize: int = None
    flagSet1: int = None
    flagSet2: int = None
    maxTxdBm: int = None
    txAttnStep: int = None
    maxTxmW: int = None
    txSteps: int = None
    szTagBuffer: int = None
    curCfgMaxAnt: int = None
    curCfgMaxGPIO: int = None
    chipVersion: int = None
    moduleType: int = None
    moduleConfigFlags: int = None
    v2Level: int = None
    secChipMajorVersion: int = None
    secChipMinorVersion: int = None
    secChipMaintenanceVersion: int = None
    secChipReleaseVersion: int = None
    res: bytearray = None

    def __init__(self, c_object: _C_NUR_DEVICECAPS = None):
        super().__init__()
        if c_object is not None:
            self.from_Ctype(c_object)

    def from_Ctype(self, c_object: _C_NUR_DEVICECAPS):
        self.dwSize = c_object.dwSize
        self.flagSet1 = c_object.flagSet1
        self.flagSet2 = c_object.flagSet2
        self.maxTxdBm = c_object.maxTxdBm
        self.txAttnStep = c_object.txAttnStep
        self.maxTxmW = c_object.maxTxmW
        self.txSteps = c_object.txSteps
        self.szTagBuffer = c_object.szTagBuffer
        self.curCfgMaxAnt = c_object.curCfgMaxAnt
        self.curCfgMaxGPIO = c_object.curCfgMaxGPIO
        self.chipVersion = c_object.chipVersion
        self.moduleType = c_object.moduleType
        self.moduleConfigFlags = c_object.moduleConfigFlags
        self.v2Level = c_object.v2Level
        self.secChipMajorVersion = c_object.secChipMajorVersion
        self.secChipMinorVersion = c_object.secChipMinorVersion
        self.secChipMaintenanceVersion = c_object.secChipMaintenanceVersion
        self.secChipReleaseVersion = c_object.secChipReleaseVersion
        self.res = bytearray(c_object.res)


class _C_NUR_INVENTORYSTREAM_DATA(ctypes.Structure):
    _fields_ = [('tagsAdded', ctypes.c_int),
                ('stopped', ctypes.c_bool),
                ('roundsDone', ctypes.c_int),
                ('collisions', ctypes.c_int),
                ('Q', ctypes.c_int)]


@dataclass_json
@dataclass
class NurInventoryStreamData:
    tags_added: int = None
    stopped: bool = None
    rounds_done: int = None
    collisions: int = None
    Q: int = None

    def __init__(self, c_object: _C_NUR_INVENTORYSTREAM_DATA = None):
        super().__init__()
        if c_object is not None:
            self.from_Ctype(c_object)

    def from_Ctype(self, c_object: _C_NUR_INVENTORYSTREAM_DATA):
        self.tags_added = c_object.tagsAdded
        self.stopped = c_object.stopped
        self.rounds_done = c_object.roundsDone
        self.collisions = c_object.collisions
        self.Q = c_object.Q
