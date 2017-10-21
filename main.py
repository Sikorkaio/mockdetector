import click
import bluetooth


def connect_to_phone(target_name):
    target_address = None

    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        if target_name == bluetooth.lookup_name(bdaddr):
            target_address = bdaddr
            break

    if target_address is not None:
        print ("found target bluetooth device with address ", target_address)
    else:
        print ("could not find target bluetooth device nearby")


@click.option(
    '--devicename',
    required=True,
    help='Name of the bluetooth device to connect to'
)
@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx, **kwargs):
    connect_to_phone(kwargs['devicename'])


if __name__ == "__main__":
    main()
