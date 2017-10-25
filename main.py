import time
import sys
import click
from crypto import Account
from bt_server import connect_to_phone, run_bt_server



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
@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx, action, **kwargs):
    check_input(action, kwargs)
    if action == 'connect-to-phone':
        if 'devicename' in kwargs and kwargs['devicename'] is not None:
            connect_to_phone(kwargs['devicename'])
    elif action == 'bt-server':
        acc = Account(kwargs['keyfile'], kwargs['passfile'])
        run_bt_server(acc)
    elif action == 'keysign':
        acc = Account(kwargs['keyfile'], kwargs['passfile'])
        data = acc.create_signed_message(
            kwargs['user_address'],
            int(time.time()),
        )
        print(data)


def check_input(action, kwargs):
    if action == 'connect-to-phone':
        return

    if 'keyfile' not in kwargs or kwargs['keyfile'] is None:
        print("For keysign you should provide an ethereum keyfile")
        sys.exit(1)
    if 'passfile' not in kwargs or kwargs['passfile'] is None:
        print("For keysign you should provide a password file for the key")
        sys.exit(1)
    if 'user_address' not in kwargs or kwargs['user_address'] is None:
        print("For keysign you should provide a user-address")
        sys.exit(1)


if __name__ == "__main__":
    main()
