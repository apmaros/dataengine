import sys

from werkzeug.security import generate_password_hash

HASH_METHOD = 'sha256'

if len(sys.argv) != 2:
    print("Error: accepts exactly one parameter")
    print(f"Usage: {sys.argv[0]} <password>")
    exit(1)

hashed_password = generate_password_hash(sys.argv[1], HASH_METHOD)

print(hashed_password)
