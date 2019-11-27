'''
Implement the fernet algorithm from pycryptography
'''
# Import python libs
import hashlib
import base64
# Import third party libs
import cryptography.fernet


async def setup(hub, unit, seal_raw):
    '''
    Using the seal data derive a key
    '''
    seal_raw = seal_raw.encode()
    seal = hub.takara.UNITS[unit]['seal']
    if getattr(hub, f'takara.seal.{seal}.ENCODE_RAW'):
        key = base64.urlsafe_b64encode(hashlib.blake2s(seal_raw).digest())
    else:
        key = seal_raw
    hub.takara.UNITS[unit]['cipher'] = cryptography.fernet.Fernet(key)


async def encrypt(hub, unit, data):
    '''
    Using the key from the given unit encrypt the raw bytes found in data
    and return the encryption string
    '''
    cipher = hub.takara.UNITS[unit]['cipher']
    return cipher.encrypt(data)


async def decrypt(hub, unit, data):
    '''
    Using the key from the given unit decrypt the raw bytes found in data
    and return the clear string
    '''
    cipher = hub.takara.UNITS[unit]['cipher']
    return cipher.decrypt(data)

