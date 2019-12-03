__virtualname__ = 'shamir'
# Import python libs
import os
import codecs
import base64
import hashlib
from getpass import getpass

# Import third party libs
import cryptography.fernet

# Tell takara to present the seal_raw to the end user, as the seal can only
# be generated
EXPOSE_SEAL_RAW = True

# Computation variables
SECRET_LEN = 32
POLY = 115792089237316195423570985008687907853269984665640564039457584007913129640997
CHECK = b'Oh king eh? Very nice!'


async def get(hub, seal_raw=None, cipher=None):
    if seal_raw is not None:
        return seal_raw
    first = getpass('Please enter the first of three keys: ')
    second = getpass('Please enter the second of three keys: ')
    third = getpass('Please enter the third of three keys: ')
    return '{first}:{second}:{third}'


async def gen(hub, seal_raw=None, cipher=None):
    if seal_raw is not None:
        return seal_raw
    key = getattr(hub, f'takara.cipher.{cipher}.gen')()
    comps = split(key, 5, 3)
    ret = ''
    for comp in comps:
        ret += f'{comp[0]}|{comp[1].hex()}:'
    return ret[:-1]


async def create(hub, **kw):
    comps = _to_comps(kw['seal_raw'].encode('utf-8'))
    secret = combine(3, comps)
    key = base64.urlsafe_b64encode(hashlib.blake2s(secret).digest())
    crypter = cryptography.fernet.Fernet(key)
    return crypter.encrypt(CHECK)


async def verify(hub, passwd, phash):
    '''
    Verify that the key derived from the source is good
    '''
    comps = _to_comps(passwd.encode('utf-8'))
    secret = combine(3, comps)
    key = base64.urlsafe_b64encode(hashlib.blake2s(secret).digest())
    crypter = cryptography.fernet.Fernet(key)
    if crypter.decrypt(phash) == CHECK:
        return True
    return False


def derive(hub, seal_raw):
    '''
    Derive the correct key from the seal_raw inputs
    '''
    comps = _to_comps(seal_raw)
    secret = combine(3, comps)
    key = base64.urlsafe_b64encode(hashlib.blake2s(secret).digest())
    return key


def _to_comps(seal_raw):
    ret = []
    for comp in seal_raw.split(b':'):
        num, hex_digest = comp.split(b'|')
        ret.append((int(num), bytes.fromhex(hex_digest.decode())))
    return ret


def hexdec(data):
    return codecs.getdecoder('hex')(data)[0]


def hexenc(data):
    return codecs.getencoder('hex')(data)[0].decode('utf-8')


def bytes_to_long(raw):
    return int(hexenc(raw), 16)


def long_to_bytes(n, size=32):
    res = hex(int(n))[2:].rstrip("L")
    if len(res) % 2 != 0:
        res = "0" + res
    s = hexdec(res)
    if len(s) != size:
        s = (size - len(s)) * b"\x00" + s
    return s

def _lshift(x, bits):
    return x * (1 << bits)


def _field_mult(x, y):
    b = x
    z = b if y & 1 == 1 else 0
    for i in range(1, SECRET_LEN * 8):
        b = _lshift(b, 1)
        if (b >> (SECRET_LEN * 8)) & 1 == 1:
            b ^= POLY
        if y & (1 << i):
            z ^= b
    return z


def _horner(t, x, coef):
    y = coef[t - 1]
    for i in range(t - 1, 0, -1):
        y = _field_mult(y, x)
        y ^= coef[i - 1]
    return y


def _field_invert(x):
    u, v = x, POLY
    g, z = 0, 1
    while u > 1:
        i = len(bin(u)[2:]) - len(bin(v)[2:])
        if i < 0:
            u, v = v, u
            z, g = g, z
            i = -i
        u = u ^ _lshift(v, i)
        z = z ^ _lshift(g, i)
    return z


def _calculate_li0(t, x, i):
    li0 = 1
    for j in range(t):
        if j == i:
            continue
        li0 = _field_mult(li0, x[j])
        li0 = _field_mult(li0, _field_invert(x[i] ^ x[j]))
    return li0


def split(secret, n, t):
    '''
    Split the given secret, n being the number of required keys
    and t being the total number of keys
    '''
    coef = [bytes_to_long(secret[::-1])]
    if n < 0 or t < 0 or n < t or not secret:
        raise ValueError('Invalid parameters specified')
    for i in range(1, t):
        coef.append(bytes_to_long(os.urandom(SECRET_LEN)))
    out = []
    for i in range(1, n + 1):
        out.append((i, long_to_bytes(_horner(t, i, coef))[::-1]))
    return out


def combine(t, parts):
    '''
    Combine the secret from the parts given
    '''
    if t <= 0 or not parts:
        raise ValueError('Invalid parameters specified')
    if len(parts) != len(set(s[1] for s in parts)):
        raise ValueError('Equal parts found')
    x, y = list(zip(*[(s[0], bytes_to_long(s[1][::-1])) for s in parts]))
    sec = 0
    for i in range(t):
        li0 = _calculate_li0(t, x, i)
        li0si = _field_mult(li0, y[i])
        sec = sec ^ li0si
    return long_to_bytes(sec)[::-1]
