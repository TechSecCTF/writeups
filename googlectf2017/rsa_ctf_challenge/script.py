#!/usr/local/bin/python3
import binascii
import hashlib
import base64
import math

# number theory functions

def int_to_bytes(n):
  byte_length = math.ceil(n.bit_length() / 8.0)
  return n.to_bytes(byte_length, 'big')

def extended_gcd(aa, bb):
  lastremainder, remainder = abs(aa), abs(bb)
  x, lastx, y, lasty = 0, 1, 1, 0
  while remainder:
    lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
    x, lastx = lastx - quotient*x, x
    y, lasty = lasty - quotient*y, y
  return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
  g, x, y = extended_gcd(a, m)
  if g != 1:
    raise ValueError
  return x % m

# computes the cube root of a mod m
# where t is the Euler-Totient function of m
def cube_root_mod(a, m, t):
  y = modinv(3, t)
  return pow(a, y, m)

# computes the floor of the kth root of n
# uses newton's method
def iroot(k, n):
  u, s = n, n+1
  while u < s:
    s = u
    t = (k-1) * s + n // pow(s, k-1)
    u = t // k
  return s

# The RSA key is actually not needed at all in the solution
# other than to verify that it is a 1024 bit public key modulus
# and that the public exponent is 3
key = """-----BEGIN RSA PUBLIC KEY-----
MIGdMA0GCSqGSIb3DQEBAQUAA4GLADCBhwKBgQDXnmZBhgORgRu6gXwGplTHHIfV
Z1kXgC/o3cSDl8JbK14wMn3o3CPIlhbDFuyzapB3rkKcECP3uGKco4AoBf/CQDoH
ZJii5gL9YwXnUPul2wWCvTy2NyW0fkBpZwK85HtR4D6AwhHaCP6hhMPdj41spp4O
q6xbZ1E1zypmjToxVQIBAw==
-----END RSA PUBLIC KEY-----"""

if __name__ == '__main__':
  # First compute the required end of message block
  asn_prefix = b'003020300c06082a864886f70d020505000410'
  md5_hash = hashlib.md5(b'challenge').hexdigest()
  data = asn_prefix + md5_hash.encode('utf-8')
  d = int(data, 16)

  # Next compute the cube root of this number modulo 2^280
  bits = 280
  m = pow(2, bits)
  t = pow(2, bits) - pow(2, bits - 1)
  z = cube_root_mod(d, m, t)

  # Pick a number between (2^1008)^(1/3) and (2*2^1008)^(1/3) and adjust
  # it to equal to z modulo 2^280
  i = 1 # some i's produce blocks with extra null bytes; adjust until lucky
  x = iroot(3, 2 * pow(2, 1008))
  x = x - (x % m) + z - i*m

  # Check that the cube of x matches the PKCS1v1.5 format:
  y = pow(x, 3)
  signature = int_to_bytes(y)
  assert len(signature) == 127 # leading byte is 00
  assert signature[0] == 1 # second byte is 01
  assert binascii.hexlify(signature).endswith(data) # ends in asn prefix + hash
  assert 0 not in signature[:-len(data)//2] # no zero byte until the asn prefix

  # Print out base64 version of "encrypted" signature
  print(base64.b64encode(int_to_bytes(x)).decode('utf-8'))
