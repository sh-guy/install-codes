# Python3 compatible Link Key generator from Zigbee Install Code

import binascii
from crccheck.crc import CrcX25
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import ECB

def aes_mmo_hash_update(length: int, result: bytes, data: bytes) -> tuple[int, bytes]:
    block_size = AES.block_size // 8

    while len(data) >= block_size:
        block = bytes(data[:block_size])

        # Encrypt
        aes = Cipher(AES(bytes(result)), ECB()).encryptor()
        result = bytearray(aes.update(block) + aes.finalize())

        # XOR plaintext into ciphertext
        for i in range(block_size):
            result[i] ^= block[i]

        data = data[block_size:]
        length += block_size

    return (length, result)


def aes_mmo_hash(data: bytes):
    block_size = AES.block_size // 8

    result_len = 0
    remaining_length = 0
    length = len(data)
    result = bytearray([0] * block_size)
    temp = bytearray([0] * block_size)

    if data and length > 0:
        remaining_length = length & (block_size - 1)
        if length >= block_size:
            hashed_length = length & ~(block_size - 1)
            (result_len, result) = aes_mmo_hash_update(result_len, result, data)
            data = data[hashed_length:]

    for i in range(remaining_length):
        temp[i] = data[i]

    temp[remaining_length] = 0x80
    result_len += remaining_length

    if (block_size - remaining_length) < 3:
        (result_len, result) = aes_mmo_hash_update(result_len, result, temp)

        result_len -= block_size
        temp = bytearray([0] * block_size)

    bit_size = result_len * 8
    temp[block_size - 2] = (bit_size >> 8) & 0xFF
    temp[block_size - 1] = (bit_size) & 0xFF

    (result_len, result) = aes_mmo_hash_update(result_len, result, temp)

    return result


def ic_decode(code):
    code = bytes.fromhex(code)
    if len(code) not in (8, 10, 14, 18):
        return None

    real_crc = code[-2:]
    crc = CrcX25()
    crc.process(code[:-2])
    if real_crc != crc.finalbytes(byteorder="little"):
        print('Checksum not valid.')
        sys.exit(-1)
    return aes_mmo_hash(code)

if __name__ == '__main__':
    import sys
    __usage__ = 'usage: %s <code> \nconvert install code to link key'
    if len(sys.argv) != 2:
        print(__usage__ % sys.argv[0])
        sys.exit(-1)
    code = ic_decode(sys.argv[1])
    print('Derived Link Key: ' +  binascii.b2a_hex(code).decode()) 
