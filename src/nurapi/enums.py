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


def get_frequency_mode(blf):
    if blf == 160000:
        return FREQUENCY_MODE.BLF_160
    if blf == 256000:
        return FREQUENCY_MODE.BLF_256
    if blf == 320000:
        return FREQUENCY_MODE.BLF_320


def get_frequency_from_mode(freq_mode: FREQUENCY_MODE):
    if freq_mode == FREQUENCY_MODE.BLF_160:
        return 160000
    if freq_mode == FREQUENCY_MODE.BLF_256:
        return 256000
    if freq_mode == FREQUENCY_MODE.BLF_320:
        return 320000
