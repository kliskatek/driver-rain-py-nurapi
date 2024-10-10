from tests import reader


def test_connect_serial_port_ex():
    reader.Disconnect()
    reader.ConnectSerialPortEx(port_name='COM8')
    assert reader.IsConnected()
    assert reader.Ping()


def test_connect_serial_port():
    reader.Disconnect()
    reader.ConnectSerialPort(port_numer=8)
    assert reader.IsConnected()
    assert reader.Ping()


def test_usb_autoconnect():
    reader.Disconnect()
    reader.SetUsbAutoConnect(enable=True)
    assert reader.IsConnected()
    assert reader.Ping()

