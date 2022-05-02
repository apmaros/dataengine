import binascii
import hashlib
import os
import sys

if os.environ.get('SALT') is None:
    print("Error: 'SALT' environment variable must be set")
    exit(1)

SALT = os.environ.get('SALT').encode('utf-8')

HASH_METHOD = 'sha256'

if len(sys.argv) != 2:
    print("Error: Required password parameter missing")
    print(f"Usage: python {sys.argv[0]} <password>")
    exit(1)

hashed_password = hashlib.pbkdf2_hmac(
    HASH_METHOD,
    sys.argv[1].encode('utf-8'),
    SALT,
    100000  # It is recommended to use at least 100,000 iterations of SHA-256
)

print(binascii.hexlify(hashed_password).decode('utf-8'))
