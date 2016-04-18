import socket
from hashlib import sha1
import struct

def proof_of_work(s):
  s.recv(1024)
  msg = s.recv(1024).strip()
  print(msg)
  prefix = msg[msg.index("with ") + 5 : msg.index(", of")]
  suffix = 0
  while True:
    response = prefix + 'A' + struct.pack('<I', suffix)

    if(sha1(response).digest()[-3:] == "\xff"*3):
      print("SUCCESS!")
      break
    suffix += 1

  s.send(prefix + 'A' + struct.pack('<I', suffix) + '\n')


def recvline(s):
    buf = ""
    while not buf.endswith("\n"):
        buf += s.recv(1)
    return buf

def rabit_stew(s):
  N = 81546073902331759271984999004451939555402085006705656828495536906802924215055062358675944026785619015267809774867163668490714884157533291262435378747443005227619394842923633601610550982321457446416213545088054898767148483676379966942027388615616321652290989027944696127478611206798587697949222663092494873481
  f = 16155172062598073107968676378352115117161436172814227581212799030353856989153650114500204987192715640325805773228721292633844470727274927681444727510153616642152298025005171599963912929571282929138074246451372957668797897908285264033088572552509959195673435645475880129067211859038705979011490574216118690919

  print(s.recv(1024).strip())
  print(s.recv(1024).strip())

  left = 0
  right = N - 1
  bits = 1024

  current = f

  for i in range(bits):
    current = (current * 4) % N
    s.send('{}'.format(current) + '\n')
    msg = recvline(s)

    while 'lsb' not in msg:
      msg = recvline(s)

    msg = msg.strip()
    print(msg[msg.index('lsb'):msg.index('lsb') + 8])

    # guess that 2 is a QR modulo N
    if True:
      if (left + right) % 2 == 1:
        if('lsb is 0' in msg):
          right = (left + right - 1) / 2
        else:
          left = (left + right + 1) / 2
      else:
        mid = (left + right) / 2
        if('lsb is 0' in msg):
          if ((mid << (i + 1)) % N) % 2 == 0:
            right = mid
          else:
            right = mid - 1
        else:
          if ((mid << (i + 1)) % N) % 2 == 0:
            left = mid + 1
          else:
            left = mid
    else:
      if (left + right) % 2 == 1:
        if('lsb is 1' in msg):
          right = (left + right - 1) / 2
        else:
          left = (left + right + 1) / 2
      else:
        mid = (left + right) / 2
        if('lsb is 1' in msg):
          if ((mid << (i + 1)) % N) % 2 == 0:
            right = mid
          else:
            right = mid - 1
        else:
          if ((mid << (i + 1)) % N) % 2 == 0:
            left = mid + 1
          else:
            left = mid

    if left == right:
      print("DONE")
      break

  print(left)

if __name__ == '__main__':
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(("rabit.pwning.xxx", 7763))

  proof_of_work(s)
  rabit_stew(s)
