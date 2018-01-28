'''
    InjectionPayload Decrypter
    Jan 20th 2017
'''

import binascii
import hashlib
import sys
import os


def xor_str(str1, str2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(str1, str2))


def decrypt(data, op):
    try:
        payload_data = data[data.find('0d0a0d0a') + 8:]
        data_bytes = binascii.unhexlify(payload_data)
        g = ''

        while len(g) < len(data_bytes):
            op = binascii.unhexlify(hashlib.md5(g + str(op) + 'pAsswd1').hexdigest())
            g += op[0: 8]

        return xor_str(data_bytes, g)
    except TypeError:
        return ''


def decrypt_unknown(data):
    for op in range(100000, 999999):
        decrypted = decrypt(data, op)

        print 'Trying Operation Code {0}\r'.format(op),

        if '!NF0' in decrypted:
            print '\nSuccessfully Decrypted !\nOperation Code: ' + str(op) + '\n\n' + decrypted
            return

    print 'Unable to decrypt'


if len(sys.argv) > 1:
    response_bytes_str = sys.argv[1]

    if len(sys.argv) == 3:
        operation_code = sys.argv[2]
        decrypted = decrypt(response_bytes_str, operation_code)

        print decrypted if decrypted != '' else 'Invalid operation code'

    elif len(sys.argv) == 2:
        decrypt_unknown(response_bytes_str)

else:
    print 'Usage:', os.path.basename(sys.argv[0]), '"ResponseBytes" "OperationCode <Optional>"'
