import sys
import click
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
from crypto import Account


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


def run_bt_server():
    """Adapted from: https://github.com/EnableTech/raspberry-bluetooth-demo"""
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
            if data == b'g':
                client_sock.send("YO THIS THE DETECTOR")
    except IOError:
        pass

    print("disconnected")

    client_sock.close()
    server_sock.close()
    print("all done")


@click.option(
    '--devicename',
    required=False,
    help='Name of the bluetooth device to connect to'
)
@click.option(
    '--action',
    required=False,
    help='Name of the bluetooth device to connect to'
)
@click.option(
    '--action',
    required=True,
    type=click.Choice(['connect-to-phone', 'bt-server', 'keysign']),
    help='The command to run'
)
@click.option(
    '--keyfile',
    required=False,
    help='Path to the ethereum keyfile to use'
)
@click.option(
    '--passfile',
    required=False,
    help='Path to a textfile containing the password for the ethereum keyfile'
)
@click.option(
    '--user-address',
    required=False,
    help='An address of the user for whom to create a signed message'
)
@click.option(
    '--duration',
    type=int,
    required=False,
    help='Duration for which user is considered present in secods'
)
@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx, action, **kwargs):
    if action == 'connect-to-phone':
        if 'devicename' in kwargs and kwargs['devicename'] is not None:
            connect_to_phone(kwargs['devicename'])
    elif action == 'bt-server':
        run_bt_server()
    elif action == 'keysign':
        if 'keyfile' not in kwargs or kwargs['keyfile'] is None:
            print("For keysign you should provide an ethereum keyfile")
            sys.exit(1)
        if 'passfile' not in kwargs or kwargs['passfile'] is None:
            print("For keysign you should provide a password file for the key")
            sys.exit(1)
        if 'duration' not in kwargs or kwargs['duration'] is None:
            print("For keysign you should provide a duration")
            sys.exit(1)
        if 'user_address' not in kwargs or kwargs['user_address'] is None:
            print("For keysign you should provide a user-address")
            sys.exit(1)

        acc = Account(kwargs['keyfile'], kwargs['passfile'])
        data = acc.create_signed_message(
            kwargs['user_address'],
            kwargs['duration']
        )
        print(data)



if __name__ == "__main__":
    main()
