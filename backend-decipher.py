'''
    InjectionPayload Decrypter
    February 4th 2017
'''

import binascii
import hashlib
import sys
import os
import urllib


def xor_str(str1, str2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(str1, str2))


def decrypt(data, op):
    try:
        g = ''

        while len(g) < len(data):
            op = binascii.unhexlify(hashlib.md5(g + str(op) + 'q1w2e3r4').hexdigest())
            g += op[0: 8]

        return xor_str(data, g)
    except TypeError:
        return ''


def safe_base64_decode(data):
    missing_padding = len(data) % 4

    if missing_padding != 0:
        data += b'=' * (4 - missing_padding)

    return data.decode('base64')


param_names = {
    0: 'HTTP_USER_AGENT',
    1: 'HTTP_REFERER',
    2: 'REMOTE_ADDR',
    3: 'HTTP_HOST',
    4: 'PHP_SELF'
}

if len(sys.argv) == 3:
    response_data = urllib.unquote(urllib.unquote(sys.argv[1]))
    operation_code = sys.argv[2]
    params = response_data.split('.')

    for i, param in enumerate(params):
        plain_param = safe_base64_decode(param)
        decrypted_param = decrypt(plain_param, operation_code)

        if decrypted_param != '':
            param_name = param_names[i] if i in param_names else 'UNKNOWN'
            print param_name, ':', decrypted_param

else:
    print 'Usage:', os.path.basename(sys.argv[0]), '"RequestData" "OperationCode"'
