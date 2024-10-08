from enum import Enum, auto


class OperationResult(Enum):
    SUCCESS = True
    ERROR = False


class NurBank(Enum):
    NUR_BANK_PASSWD = 0
    NUR_BANK_EPC = 1
    NUR_BANK_TID = 2
    NUR_BANK_USER = 3


class NUR_NOTIFICATION(Enum):
    NUR_NOTIFICATION_NONE = 0
    NUR_NOTIFICATION_LOG = auto()
    NUR_NOTIFICATION_PERIODIC_INVENTORY = auto()
    NUR_NOTIFICATION_PRGPRGRESS = auto()
    NUR_NOTIFICATION_TRDISCONNECTED = auto()
    NUR_NOTIFICATION_MODULEBOOT = auto()
    NUR_NOTIFICATION_TRCONNECTED = auto()
    NUR_NOTIFICATION_TRACETAG = auto()
    NUR_NOTIFICATION_IOCHANGE = auto()
    NUR_NOTIFICATION_TRIGGERREAD = auto()
    NUR_NOTIFICATION_HOPEVENT = auto()
    NUR_NOTIFICATION_INVENTORYSTREAM = auto()
    NUR_NOTIFICATION_INVENTORYEX = auto()
    NUR_NOTIFICATION_DEVSEARCH = auto()
    NUR_NOTIFICATION_CLIENTCONNECTED = auto()
    NUR_NOTIFICATION_CLIENTDISCONNECTED = auto()
    NUR_NOTIFICATION_EASALARM = auto()
    NUR_NOTIFICATION_EPCENUM = auto()
    NUR_NOTIFICATION_EXTIN = auto()
    NUR_NOTIFICATION_GENERAL = auto()
    NUR_NOTIFICATION_TUNEEVENT = auto()
    NUR_NOTIFICATION_WLAN_SEARCH = auto()
    NUR_NOTIFICATION_TT_STREAM = auto()
    NUR_NOTIFICATION_TT_CHANGED = auto()
    NUR_NOTIFICATION_TT_SCANEVENT = auto()
    NUR_NOTIFICATION_DIAG_REPORT = auto()
    NUR_NOTIFICATION_ACCESSORY = auto()
    NUR_NOTIFICATION_LAST = auto()


class NUR_MODULESETUP_FLAGS(Enum):
    NUR_SETUP_LINKFREQ = (1 << 0)  # linkFreq field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_RXDEC = (1 << 1)  # rxDecoding field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_TXLEVEL = (1 << 2)  # txLevel field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_TXMOD = (1 << 3)  # txModulation field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_REGION = (1 << 4)  # regionId field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_INVQ = (1 << 5)  # inventoryQ field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_INVSESSION = (1 << 6)  # inventorySession field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_INVROUNDS = (1 << 7)  # inventoryRounds field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_ANTMASK = (1 << 8)  # antennaMask field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_SCANSINGLETO = (1 << 9)  # scanSingleTriggerTimeout field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_INVENTORYTO = (1 << 10)  # inventoryTriggerTimeout field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_SELECTEDANT = (1 << 11)  # selectedAntenna field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_OPFLAGS = (1 << 12)  # opFlags field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_INVTARGET = (1 << 13)  # inventoryTarget field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_INVEPCLEN = (1 << 14)  # inventoryEpcLength field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_READRSSIFILTER = (1 << 15)  # readRssiFilter field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_WRITERSSIFILTER = (1 << 16)  # writeRssiFilter field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_INVRSSIFILTER = (1 << 17)  # inventoryRssiFilter field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_READTIMEOUT = (1 << 18)  # readTO field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_WRITETIMEOUT = (1 << 19)  # writeTO field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_LOCKTIMEOUT = (1 << 20)  # lockTO field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_KILLTIMEOUT = (1 << 21)  # killTO field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_AUTOPERIOD = (1 << 22)  # stixPeriod field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_PERANTPOWER = (1 << 23)  # antPower field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_PERANTOFFSET = (1 << 24)  # powerOffset field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_ANTMASKEX = (1 << 25)  # antennaMaskEx field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_AUTOTUNE = (1 << 26)  # autotune field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_PERANTPOWER_EX = (1 << 27)  # antPowerEx field in struct NUR_MODULESETUP is valid */
    NUR_SETUP_RXSENS = (1 << 28)  # rxSensitivity field in struct NUR_MODULESETUP is valid */

    # ADDED NUR2 7.0
    NUR_SETUP_RFPROFILE = (1 << 29)  # rfProfile field in struct NUR_MODULESETUP is valid */

    # ADDED NUR2 7.5, NanoNur 10.2
    NUR_SETUP_TO_SLEEP_TIME = (1 << 30)  # toSleepTime field in struct NUR_MODULESETUP is valid */

    NUR_SETUP_ALL = ((1 << 31) - 1)  # All setup flags in the structure. */


class SETUP_RX_DEC(Enum):
    FM0 = 0
    MILLER_2 = 1
    MILLER_4 = 2
    MILLER_8 = 3


class SETUP_LINK_FREQ(Enum):
    BLF_160 = 160000
    BLF_256 = 256000
    BLF_320 = 320000


class FREQUENCY_MODE(Enum):
    BLF_160 = 'BLF_160'
    BLF_256 = 'BLF_256'
    BLF_320 = 'BLF_320'


class SETUP_RF_PROFILE(Enum):
    ROBUST = 0
    NOMINAL = 1
    HIGH_SPEED = 2


class SETUP_REGION(Enum):
    EU = 0
    FCC = 1
    PRC = 2
    Malaysia = 3
    Brazil = 4
    Australia = 5
    NewZealand = 6
    Japan_250mW_LBT = 7
    Japan_500mW_DRM = 8
    Korea_LBT = 9
    India = 10
    Russia = 11
    Vietnam = 12
    Singapore = 13
    Thailand = 14
    Philippines = 15
    Morocco = 16
    Peru = 17


class NUR_LOG(Enum):
    NUR_LOG_VERBOSE = 0b0001
    NUR_LOG_ERROR = 0b0010
    NUR_LOG_USER = 0b0100
    NUR_LOG_DATA = 0b1000
    NUR_LOG_ALL = 0b1111


class NUR_ERRORCODES(Enum):
    UNKNOWN_ERROR = -1
    # Call succeeded
    NUR_SUCCESS = 0
    # Invalid command sent to module
    NUR_ERROR_INVALID_COMMAND = auto()
    # Invalid packet length sent to module
    NUR_ERROR_INVALID_LENGTH = auto()
    # Command parameter(s) out of range
    NUR_ERROR_PARAMETER_OUT_OF_RANGE = auto()
    # Data receive timeout
    NUR_ERROR_RECEIVE_TIMEOUT = auto()
    # Invalid command parameter(s); Invalid function parameter(s)
    NUR_ERROR_INVALID_PARAMETER = auto()
    # Programming failure
    NUR_ERROR_PROGRAM_FAILED = auto()
    # Parameter mismatch
    NUR_ERROR_PARAMETER_MISMATCH = auto()
    # HW mismatch
    NUR_ERROR_HW_MISMATCH = auto()
    NUR_ERROR_RESERVED1 = auto()
    # Page programming failure
    NUR_ERROR_PAGE_PROGRAM = auto()
    # Memory check failed
    NUR_ERROR_CRC_CHECK = auto()
    # CRC mismatch in parameter
    NUR_ERROR_CRC_MISMATCH = auto()
    # Device not ready or region that is being programmed is not unlocked
    NUR_ERROR_NOT_READY = auto()
    # Module application not present
    NUR_ERROR_APP_NOT_PRESENT = auto()

    # Generic = auto() non-interpreted / unexpected error
    NUR_ERROR_GENERAL = 0x10
    # Device wants to have last packet again due to the transfer failure.
    NUR_ERROR_RESEND_PACKET = auto()

    # No tag(s) found
    NUR_ERROR_NO_TAG = 0x20
    # Air error
    NUR_ERROR_RESP_AIR = auto()
    # G2 select error
    NUR_ERROR_G2_SELECT = auto()
    # G2 select data missing
    NUR_ERROR_MISSING_SELDATA = auto()
    # G2 access error
    NUR_ERROR_G2_ACCESS = auto()

    # G2 Read error = auto() unspecified
    NUR_ERROR_G2_READ = 0x30
    # G2 Partially successful read
    NUR_ERROR_G2_RD_PART = auto()
    # G2 Write error = auto() unspecified
    NUR_ERROR_G2_WRITE = 0x40
    # G2 Partially successful write
    NUR_ERROR_G2_WR_PART = auto()
    # G2 Tag read responded w/ error
    NUR_ERROR_G2_TAG_RESP = auto()

    # Special error; Some additional debug data is returned with this error
    NUR_ERROR_G2_SPECIAL = 0x50

    # HW error
    NUR_ERROR_READER_HW = 0x60
    # Antenna too bad
    NUR_ERROR_BAD_ANTENNA = auto()
    # Low voltage
    NUR_ERROR_LOW_VOLTAGE = auto()
    # Over temperature
    NUR_ERROR_OVER_TEMP = auto()

    # Invalid handle passed to function
    NUR_ERROR_INVALID_HANDLE = 0x1000
    # Transport error
    NUR_ERROR_TRANSPORT = auto()
    # Transport not connected
    NUR_ERROR_TR_NOT_CONNECTED = auto()
    # Transport timeout
    NUR_ERROR_TR_TIMEOUT = auto()
    # Buffer too small
    NUR_ERROR_BUFFER_TOO_SMALL = auto()
    # Functionality not supported
    NUR_ERROR_NOT_SUPPORTED = auto()
    # Packet contains no payload
    NUR_ERROR_NO_PAYLOAD = auto()
    # Packet is invalid
    NUR_ERROR_INVALID_PACKET = auto()
    # Packet too long
    NUR_ERROR_PACKET_TOO_LONG = auto()
    # Packet Checksum failure
    NUR_ERROR_PACKET_CS_ERROR = auto()
    # Data not in WORD boundary
    NUR_ERROR_NOT_WORD_BOUNDARY = auto()
    # File not found
    NUR_ERROR_FILE_NOT_FOUND = auto()
    # File error; not in NUR format
    NUR_ERROR_FILE_INVALID = auto()
    # NUR file and module's MCU architecture mismatch
    NUR_ERROR_MCU_ARCH = auto()

    # The specified memory location does not exists or the EPC length field is not supported by the tag
    NUR_ERROR_G2_TAG_MEM_OVERRUN = auto()
    # The specified memory location is locked and/or permalocked and is either not writeable or not readable
    NUR_ERROR_G2_TAG_MEM_LOCKED = auto()
    # The tag has insufficient power to perform the memory-write operation
    NUR_ERROR_G2_TAG_INSUF_POWER = auto()
    # The tag does not support error-specific codes
    NUR_ERROR_G2_TAG_NON_SPECIFIC = auto()
    # Transport suspended error
    NUR_ERROR_TR_SUSPENDED = auto()
    # TCP/IP Server error
    NUR_ERROR_SERVER = auto()
    # Device query is busy.
    NUR_ERROR_QUERY_BUSY = auto()
    # Tag backscattered error code 0x00: "catch all" error.
    NUR_ERROR_G2_TAG_OTHER_ERROR = auto()
    # Tag backscattered error code 0x01: not supported parameters or feature.
    NUR_ERROR_G2_TAG_NOT_SUPPORTED = auto()
    # Tag backscattered error code 0x04: insufficient priviledge.
    NUR_ERROR_G2_TAG_INSUF_PRIVILEDGE = auto()
    # Tag backscattered error code 0x05: cryptographic suite error.
    NUR_ERROR_G2_TAG_CRYPTO_SUITE = auto()
    # Tag backscattered error code 0x06: command was not encapsulated in AuthComm or SecureComm.
    NUR_ERROR_G2_TAG_NOT_ENCAPSULATED = auto()
    # Tag backscattered error code 0x07: ResponseBuffer overflowed.
    NUR_ERROR_G2_TAG_RESPBUFFER_OVF = auto()
    # Tag backscattered error code 0x10: failure because of security timeout.
    NUR_ERROR_G2_TAG_SEC_TIMEOUT = auto()
