'''
    'infol' Param Decrypter
    Jan 22th 2017
'''

import binascii
import hashlib
import urllib
import sys
import os


def xor_str(str1, str2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(str1, str2))


def decrypt(infol_base64):
    infol_str = infol_base64.decode('base64')
    seq = 'pAsswd1'
    g = ''

    while len(g) < len(infol_str):
        seq = binascii.unhexlify(hashlib.md5(g + seq + '123456790').hexdigest())
        g += seq[0: 8]

    return xor_str(infol_str, g)


if len(sys.argv) > 1:
    infol_b64 = urllib.unquote(sys.argv[1]).decode('utf8')
    print decrypt(infol_b64)
else:
    print 'Usage:', os.path.basename(sys.argv[0]), '"infol B64 String"'
