import time
from bluetooth import (
    BluetoothSocket,
    RFCOMM,
    PORT_ANY,
    SERIAL_PORT_CLASS,
    SERIAL_PORT_PROFILE,
    advertise_service,
    discover_devices,
    lookup_name,
)


def connect_to_phone(target_name):
    target_address = None

    nearby_devices = discover_devices()
    for bdaddr in nearby_devices:
        if target_name == lookup_name(bdaddr):
            target_address = bdaddr
            break

    if target_address is not None:
        print ("found target bluetooth device with address ", target_address)
    else:
        print ("could not find target bluetooth device nearby")


def run_bt_server(account):
    """Adapted from: https://github.com/EnableTech/raspberry-bluetooth-demo"""
    import pdb
    pdb.set_trace()
    server_sock = BluetoothSocket(RFCOMM)

    server_sock.bind(("", PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]
    print ("listening on port %d" % port)

    uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
    advertise_service(
        server_sock,
        "Mock Detector",
        service_id=uuid,
        service_classes=[uuid, SERIAL_PORT_CLASS],
        profiles=[SERIAL_PORT_PROFILE],
        # protocols=[OBEX_UUID],
    )

    print("Waiting for connection on RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    try:
        while True:
            data = client_sock.recv(1024)
            if len(data) == 0:
                break
            print("received [%s]" % data)
            if data == b'ETH_ADDRESS\r\n':
                client_sock.send(
                    "ETH_ADDRESS::0x{}\r\nEND\r\n".format(account.address())
                )
            elif data.startswith('SIGNED_MESSAGE::'):
                start = len('SIGNED_MESSAGE::')
                user_address = data[start:start+42]
                message = account.create_signed_message(
                    user_address,
                    int(time.time())
                )
                client_sock.send(message)
    except IOError:
        pass

    print("disconnected")

    client_sock.close()
    server_sock.close()
    print("all done")
