import binascii
import struct

w = binascii.unhexlify('220f02c883fbe083c0200f10cd0013b8')
m = binascii.unhexlify('ffffffffffffff00ffffffffffffff00')
z = binascii.unhexlify('000000000000032900000000000002d6')

constraints = [
                '70021102',
                '55022902',
                '91025e02',
                '3302f901',
                '78027b02',
                '21020902',
                '5d029002',
                '8f02df02'
              ]

variables = [chr(ord('a') + i) for i in range(16)]

constraints = [struct.unpack('<I', binascii.unhexlify(c))[0] for c in constraints]
constraints = constraints[::-1]

def printz(c):
  s1 = c % (1 << 0x10)
  s2 = (c - s1) >> (0x10)
  w = struct.pack('>Q', s1) + struct.pack('>Q', s2)
  return binascii.hexlify(w)

def print_constraints():
  for i in range(7, -1, -1):
    c = constraints[i-1]
    z = binascii.unhexlify(printz(c))
    if i == 0:
      z = w
    s = ''
    q = constraints[i]
    s1 = q % (1 << 0x10)
    s2 = (q - s1) >> (0x10)
    for j in range(8):
      if j == 7-i:
        s += 'abs(0-' + str(ord(z[j])) + ') + '
        continue
      s += 'abs(' + variables[j] + '-' + str(ord(z[j])) + ') + '
    s += '0 == {}, '.format(s1)
    print(s)
    s = ''
    for j in range(8,16):
      if j-8 == 7-i:
        s += 'abs(0-' + str(ord(z[j])) + ') + '
        continue
      s += 'abs(' + variables[j] + '-' + str(ord(z[j])) + ') + '
    s += '0 == {}, '.format(s2)
    print(s)

if __name__ == '__main__':
  print_constraints()
