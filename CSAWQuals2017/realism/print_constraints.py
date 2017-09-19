import binascii
import struct

# Initial value of xmm5
xmm5_start = binascii.unhexlify('220f02c883fbe083c0200f10cd0013b8')

# The data stored at 0x7DA8 and compared against esi
esi_consts = [
                '70021102',
                '55022902',
                '91025e02',
                '3302f901',
                '78027b02',
                '21020902',
                '5d029002',
                '8f02df02'
              ]
esi_consts = [struct.unpack('<I', binascii.unhexlify(c))[0] for c in esi_consts]
esi_consts = esi_consts[::-1]

# Our 16 variables ('a' through 'p')
variables = [chr(ord('a') + i) for i in range(16)]

def esi_to_xmm5(esi):
  s1 = esi % (1 << 0x10)
  s2 = (esi - s1) >> (0x10)
  w = struct.pack('>Q', s1) + struct.pack('>Q', s2)
  return w

def print_constraints():
  for i in range(8):
    prev_esi = esi_consts[i-1]
    xmm5 = esi_to_xmm5(prev_esi)
    if i == 0:
      xmm5 = xmm5_start

    esi = esi_consts[i]
    s1 = esi % (1 << 0x10)
    s2 = (esi - s1) >> (0x10)

    # sum of absolute differences between xmm5 and our flag
    s = ''
    for j in range(8):
      if j == 7-i:
        # This is the masking step
        s += 'abs(0-' + str(ord(xmm5[j])) + ') + '
        continue
      s += 'abs(' + variables[j] + '-' + str(ord(xmm5[j])) + ') + '
    s += '0 == {}, '.format(s1)
    print(s)

    s = ''
    for j in range(8,16):
      if j-8 == 7-i:
        # This is the masking step
        s += 'abs(0-' + str(ord(xmm5[j])) + ') + '
        continue
      s += 'abs(' + variables[j] + '-' + str(ord(xmm5[j])) + ') + '
    s += '0 == {}, '.format(s2)
    print(s)

if __name__ == '__main__':
  print_constraints()
