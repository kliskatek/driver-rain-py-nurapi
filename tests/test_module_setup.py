from src.nurapi import NurModuleSetup
from src.nurapi.enums import SETUP_LINK_FREQ, SETUP_RX_DEC, NUR_MODULESETUP_FLAGS
from tests import reader

device_caps = reader.GetDeviceCaps()
reader_info = reader.GetReaderInfo()


def test_communication_mode():
    for link_freq in SETUP_LINK_FREQ:
        for rx_dec in SETUP_RX_DEC:
            module_setup = NurModuleSetup()
            module_setup.link_freq = link_freq
            module_setup.rx_decoding = rx_dec
            reader.SetModuleSetup(
                setup_flags=[
                    NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
                    NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC
                ],
                module_setup=module_setup)

            module_setup = reader.GetModuleSetup(
                setup_flags=[
                    NUR_MODULESETUP_FLAGS.NUR_SETUP_LINKFREQ,
                    NUR_MODULESETUP_FLAGS.NUR_SETUP_RXDEC
                ])
            assert module_setup.link_freq == link_freq
            assert module_setup.rx_decoding == rx_dec


def test_antenna():
    for antenna_idx in range(reader_info.num_antennas):
        module_setup = NurModuleSetup()
        module_setup.antenna_mask_ex = 0b1 << antenna_idx
        module_setup.selected_antenna = -1  # Automatic selection
        reader.SetModuleSetup(
            setup_flags=[
                NUR_MODULESETUP_FLAGS.NUR_SETUP_ANTMASKEX,
                NUR_MODULESETUP_FLAGS.NUR_SETUP_SELECTEDANT
            ],
            module_setup=module_setup)

        module_setup = reader.GetModuleSetup(
            setup_flags=[
                NUR_MODULESETUP_FLAGS.NUR_SETUP_ANTMASKEX,
                NUR_MODULESETUP_FLAGS.NUR_SETUP_SELECTEDANT
            ])
        assert module_setup.antenna_mask_ex == 0b1 << antenna_idx
        assert module_setup.selected_antenna == -1


def test_power():
    tx_options = range(device_caps.maxTxdBm - (device_caps.txAttnStep - 1) * device_caps.txSteps,
                       device_caps.maxTxdBm,
                       device_caps.txAttnStep)
    for tx_dbm in tx_options:
        module_setup = NurModuleSetup()
        module_setup.tx_level = ((device_caps.maxTxdBm - tx_dbm) *
                                 device_caps.txAttnStep)
        reader.SetModuleSetup(
            setup_flags=[
                NUR_MODULESETUP_FLAGS.NUR_SETUP_TXLEVEL
            ],
            module_setup=module_setup)

        module_setup = reader.GetModuleSetup(
            setup_flags=[
                NUR_MODULESETUP_FLAGS.NUR_SETUP_TXLEVEL
            ])
        assert module_setup.tx_level == tx_dbm
