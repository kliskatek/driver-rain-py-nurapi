from src.nurapi import NurBank
from tests import reader, present_tag_epc


def test_read():
    for address in [0, 1, 2, 3]:
        for data in [0x1234, 0x5678]:
            reader.WriteTagByEPC(passwd=0,
                                 secured=False,
                                 epc=present_tag_epc,
                                 bank=NurBank.NUR_BANK_USER,
                                 address=address,
                                 byte_count=2,
                                 data=data.to_bytes(2, byteorder='big'))
            data_read = reader.ReadTagByEPC(passwd=0,
                                            secured=False,
                                            epc=present_tag_epc,
                                            bank=NurBank.NUR_BANK_USER,
                                            address=address,
                                            byte_count=2)
            assert data_read == data.to_bytes(2, byteorder='big')
