import binascii
import json
import struct
from ethereum.tools.keys import decode_keystore_json
from coincurve import PrivateKey
from sha3 import keccak_256


def sha3(data):
    """
    Raises:
        RuntimeError: If Keccak lib initialization failed, or if the function
        failed to compute the hash.

        TypeError: This function does not accept unicode objects, they must be
        encoded prior to usage.
    """
    return keccak_256(data).digest()


def address_decoder(addr):
    if addr[:2] == '0x':
        addr = addr[2:]

    addr = binascii.unhexlify(addr)
    assert len(addr) in (20, 0)
    return addr


class Account(object):

    def __init__(self, keyfile, passfile):
        with open(keyfile) as data_file:
            data = json.load(data_file)

        with open(passfile) as f:
            password = f.read().strip('\n')

        privkey_bin = decode_keystore_json(data, password)
        self.private_key = PrivateKey(privkey_bin)

    def address(self):
        return binascii.hexlify(bytearray(
            sha3(self.private_key.public_key.format(
                compressed=False)[1:])[-20:]
        ))

    def sign(self, messagedata):
        signature = self.private_key.sign_recoverable(
            messagedata,
            hasher=sha3
        )
        if len(signature) != 65:
            raise ValueError('invalid signature')

        return signature[:-1] + bytearray(chr(signature[-1] + 27), 'utf-8')

    def create_signed_message(self, user_address_hex, duration_seconds):
        message_data = (
            bytearray(address_decoder(user_address_hex)) +
            bytearray(struct.pack("L", duration_seconds))
        )
        sig = self.sign(message_data)
        message_data = message_data + bytearray(sig)
        return message_data
