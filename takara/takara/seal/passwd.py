'''
The most simple seal, a password. The password is stored in a salted hash in
the unit config. The password itself is used to create a seperate key for the
given cipher.

This implementation uses PBKDF2, this is not nessisarily the best choice, but
it is highly portable, well supported and has a great track record. It is
also natively available inside of the standard python library.

If other password implementations are desired we plan to add vertical app
merged systems to support argon2, bcrypt, and scrypt.
'''
# Import python libs
import hashlib
import binascii
import random
import time
import os
from getpass import getpass

# Don't echo the password back to the user
EXPOSE_SEAL_RAW = False
ENCODE_RAW = True


async def gen(hub, seal_raw=None, cipher=None):
    '''
    Generate a password, in this case, gather the password from the cli unless
    a password is provided
    '''
    if seal_raw is not None:
        return seal_raw
    return getpass()


async def create(hub, **kw):
    '''
    Given a password, create the salted hash to store for verification. This
    function is not unit specific but it intended to be called before the
    unit itself is created with the result passed down to the unit creation.
    '''
    algo = kw.get('passwd_hash_algo', 'sha512')
    iterations = kw.get('passwd_iterations', 100000)
    passwd = kw['seal_raw'].encode('utf-8')
    salt = os.urandom(1024)
    raw = hashlib.pbkdf2_hmac(algo, passwd, salt, iterations)
    return b':'.join([
        algo.encode('utf-8'),
        binascii.hexlify(raw),
        binascii.hexlify(salt),
        str(iterations).encode('utf-8')
        ])


async def verify(hub, passwd, phash):
    '''
    Verify the given phash and password combination
    '''
    passwd = passwd.encode('utf-8')
    phash = phash
    comps = phash.split(b':')
    if len(comps) != 4:
        return False
    algo = comps[0].decode('utf-8')
    raw = binascii.unhexlify(comps[1])
    salt = binascii.unhexlify(comps[2])
    iterations = int(comps[3])
    new_raw = hashlib.pbkdf2_hmac(algo, passwd, salt, iterations)
    good = True
    for idx, part in enumerate(raw):
        if part != new_raw[idx]:
            good = False
    if not good:
        base = 0.2
        base = base + random.randint(1000, 9000) * 0.0001
        time.sleep(base)
    return good
