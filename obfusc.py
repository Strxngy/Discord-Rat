
from base64 import b64decode

def show(b):
    return b64decode(b).decode()

while True:
    hidden = b'' #base664 encode main.py
    eval(compile(show(hidden), '<string>', 'exec'))
    exit(0)