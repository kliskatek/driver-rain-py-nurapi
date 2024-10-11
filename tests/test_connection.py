from tests import reader, reader_port_name, reader_port_number


def test_connect_serial_port_ex():
    if reader.IsConnected():
        reader.Disconnect()
    reader.ConnectSerialPortEx(port_name=reader_port_name)
    assert reader.IsConnected()
    assert reader.Ping()


def test_connect_serial_port():
    if reader.IsConnected():
        reader.Disconnect()
    reader.ConnectSerialPort(port_numer=reader_port_number)
    assert reader.IsConnected()
    assert reader.Ping()


def test_usb_autoconnect():
    if reader.IsConnected():
        reader.Disconnect()
    reader.SetUsbAutoConnect(enable=True)
    assert reader.IsConnected()
    assert reader.Ping()

