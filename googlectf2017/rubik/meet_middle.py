import hashlib
import socket
import binascii

def permute(s, method):
    o = [c for c in s]
    if method == "U":
        for i in range(9, 17+1):
            o[i]=s[i+3]
        for i in range(18, 20+1):
            o[i]=s[i-9]
        o[0]=s[6]
        o[3]=s[7]
        o[6]=s[8]
        o[7]=s[5]
        o[8]=s[2]
        o[5]=s[1]
        o[2]=s[0]
        o[1]=s[3]

    elif method == "X'":
        for i in range(12,14+1):
            o[i]=s[i-12]
        for i in range(24, 26+1):
            o[i]=s[i-21]
        for i in range(36, 38+1):
            o[i]=s[i-30]
        for i in range(45, 47+1):
            o[i]=s[i-33]
        for i in range(48, 50+1):
            o[i]=s[i-24]
        for i in range(51, 53+1):
            o[i]=s[i-15]
        for i in range(18, 20+1):
            o[i]=s[71-i]
        for i in range(30, 32+1):
            o[i]=s[80-i]
        for i in range(42, 44+1):
            o[i]=s[89-i]
        for i in range(0, 2+1):
            o[i]=s[44-i]
        for i in range(3, 5+1):
            o[i]=s[35-i]
        for i in range(6, 8+1):
            o[i]=s[26-i]

        o[15]=s[17]
        o[27]=s[16]
        o[39]=s[15]
        o[40]=s[27]
        o[41]=s[39]
        o[29]=s[40]
        o[17]=s[41]
        o[16]=s[29]
        o[11]=s[9]
        o[23]=s[10]
        o[35]=s[11]
        o[34]=s[23]
        o[33]=s[35]
        o[21]=s[34]
        o[9]=s[33]
        o[10]=s[21]

    elif method == "L'":
        o[44]=s[0]
        o[32]=s[3]
        o[20]=s[6]
        o[0]=s[12]
        o[3]=s[24]
        o[6]=s[36]
        o[36]=s[51]
        o[24]=s[48]
        o[12]=s[45]
        o[51]=s[20]
        o[48]=s[32]
        o[45]=s[44]

        o[9]=s[11]
        o[10]=s[23]
        o[11]=s[35]
        o[23]=s[34]
        o[35]=s[33]
        o[34]=s[21]
        o[33]=s[9]
        o[21]=s[10]

    elif method == "L":
        o[0]=s[44]
        o[3]=s[32]
        o[6]=s[20]
        o[12]=s[0]
        o[24]=s[3]
        o[36]=s[6]
        o[51]=s[36]
        o[48]=s[24]
        o[45]=s[12]
        o[20]=s[51]
        o[32]=s[48]
        o[44]=s[45]

        o[11]=s[9]
        o[23]=s[10]
        o[35]=s[11]
        o[34]=s[23]
        o[33]=s[35]
        o[21]=s[34]
        o[9]=s[33]
        o[10]=s[21]

    elif method == "Y":
        for i in range(9, 17+1):
            o[i]=s[i+3]
        for i in range(21, 29+1):
            o[i]=s[i+3]
        for i in range(33, 41+1):
            o[i]=s[i+3]
        for i in range(18, 20+1):
            o[i]=s[i-9]
        for i in range(30, 32+1):
            o[i]=s[i-9]
        for i in range(42, 44+1):
            o[i]=s[i-9]
        o[0]=s[6]
        o[3]=s[7]
        o[6]=s[8]
        o[7]=s[5]
        o[8]=s[2]
        o[5]=s[1]
        o[2]=s[0]
        o[1]=s[3]
        o[53]=s[51]
        o[50]=s[52]
        o[47]=s[53]
        o[46]=s[50]
        o[45]=s[47]
        o[48]=s[46]
        o[51]=s[45]
        o[52]=s[48]

    elif method=="Y'":
        for i in range(12, 20+1):
            o[i]=s[i-3]
        for i in range(24, 32+1):
            o[i]=s[i-3]
        for i in range(36, 44+1):
            o[i]=s[i-3]
        for i in range(9, 11+1):
            o[i]=s[i+9]
        for i in range(21, 23+1):
            o[i]=s[i+9]
        for i in range(33, 35+1):
            o[i]=s[i+9]
        o[6]=s[0]
        o[7]=s[3]
        o[8]=s[6]
        o[5]=s[7]
        o[2]=s[8]
        o[1]=s[5]
        o[0]=s[2]
        o[3]=s[1]
        o[51]=s[53]
        o[52]=s[50]
        o[53]=s[47]
        o[50]=s[46]
        o[47]=s[45]
        o[46]=s[48]
        o[45]=s[51]
        o[48]=s[52]

    return ''.join(o)

# starting (solved) state of cube
start= "WWWWWWWWWGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBOOOYYYYYYYYY"

def MITM_ATTACK(end):
    d = {}

    cube = start
    i = 0
    while i < 1260:
        if cube not in d:
            d[cube] = []
        d[cube].append(i)
        cube = permute(permute(cube, "U"), "X'")
        i+=1

    intersect = []
    cube = end
    i = 0
    while i < 1260:
        if cube in d:
            intersect.append((d[cube][0], i))
        cube = permute(permute(cube, "Y"), "L'")
        i+=1

    return intersect

# Execute the U x' permutation reps times on state
def A_op(state, reps):
  for i in range(reps):
    state = permute(permute(state, "U"), "X'")
  return state

# Execute the L y' permutation reps times on state
def B_op(state, reps):
  for i in range(reps):
    state = permute(permute(state, "L"), "Y'")
  return state

# Given a Rubik's Cube in state s1 and another cube in state s2
# apply the permutation that takes a solved cube to s2, to s1
# i.e. if:
#   - s0 the solved Rubik's cube state
#   - p1(s0) == s1
#   - p2(s0) == s2   (where p1 and p2 are permutations)
# then this function returns p2(s1) = p2(p1(s0))
def compose(s1, s2):
  o3 = [c for c in s1]

  c1 = (s2[8], s2[14], s2[15])  # WRB
  c2 = (s2[2], s2[17], s2[18])  # WBO
  c3 = (s2[0], s2[20], s2[9])   # WOG
  c4 = (s2[6], s2[11], s2[12])  # WGR
  c5 = (s2[45], s2[36], s2[35]) # YRG
  c6 = (s2[51], s2[33], s2[44]) # YGO
  c7 = (s2[53], s2[42], s2[41]) # YOB
  c8 = (s2[47], s2[39], s2[38]) # YBR
  corners = [c1, c2, c3, c4, c5, c6, c7, c8]
  color_corners = ["WRB", "WBO", "WOG", "WGR", "YRG", "YGO", "YOB", "YBR"]

  d1 = (8, 14, 15)  # WRB
  d2 = (2, 17, 18)  # WBO
  d3 = (0, 20, 9)   # WOG
  d4 = (6, 11, 12)  # WGR
  d5 = (45, 36, 35) # YRG
  d6 = (51, 33, 44) # YGO
  d7 = (53, 42, 41) # YOB
  d8 = (47, 39, 38) # YBR
  ds = [d1, d2, d3, d4, d5, d6, d7, d8]

  e1 = (s2[7], s2[13])   # WR
  e2 = (s2[5], s2[16])   # WB
  e3 = (s2[1], s2[19])   # WO
  e4 = (s2[3], s2[10])   # WG
  e5 = (s2[23], s2[24])  # GR
  e6 = (s2[26], s2[27])  # RB
  e7 = (s2[29], s2[30])  # BO
  e8 = (s2[32], s2[21])  # OG
  e9 = (s2[37], s2[46])  # RY
  e10 = (s2[40], s2[50]) # BY
  e11 = (s2[43], s2[52]) # OY
  e12 = (s2[34], s2[48]) # GY
  edges = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12]
  color_edges = ["WR", "WB", "WO", "WG", "GR", "RB", "BO", "OG", "RY", "BY", "OY", "GY"]

  f1 = (7, 13)   # WR
  f2 = (5, 16)   # WB
  f3 = (1, 19)   # WO
  f4 = (3, 10)   # WG
  f5 = (23, 24)  # GR
  f6 = (26, 27)  # RB
  f7 = (29, 30)  # BO
  f8 = (32, 21)  # OG
  f9 = (37, 46)  # RY
  f10 = (40, 50) # BY
  f11 = (43, 52) # OY
  f12 = (34, 48) # GY
  fs = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12]

  t1 = (s2[4])
  t2 = (s2[25])
  t3 = (s2[28])
  t4 = (s2[31])
  t5 = (s2[22])
  t6 = (s2[49])
  faces = [t1, t2, t3, t4, t5, t6]
  color_faces = ["W", "R", "B", "O", "G", "Y"]


  u1 = (4,)
  u2 = (25,)
  u3 = (28,)
  u4 = (31,)
  u5 = (22,)
  u6 = (49,)
  us = [u1, u2, u3, u4, u5, u6]

  # centers

  for i in range(6):
    face = color_faces[i]
    for j in range(6):
      compare = faces[j]
      if face[0] in compare:
        break
    u1 = us[i]
    u2 = us[j]
    for z in range(1):
      y = face.index(compare[z])
      o3[u2[z]] = s1[u1[y]]

  # corners
  for i in range(8):
    corner = color_corners[i]
    for j in range(8):
      compare = corners[j]
      if corner[0] in compare and corner[1] in compare and corner[2] in compare:
        break
    d1 = ds[i]
    d2 = ds[j]
    for z in range(3):
      y = corner.index(compare[z])
      o3[d2[z]] = s1[d1[y]]

  # edges
  for i in range(12):
    edge = color_edges[i]
    for j in range(12):
      compare = edges[j]
      if edge[0] in compare and edge[1] in compare:
        break
    f1 = fs[i]
    f2 = fs[j]
    for z in range(2):
      y = edge.index(compare[z])
      o3[f2[z]] = s1[f1[y]]

  return ''.join(o3)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('rubik.ctfcompetition.com',1337))

def send(x):
  print('\033[92m' + x + '\033[0m')
  s.send(x.encode('utf-8') + b'\n')

def recv():
  q = s.recv(2048).decode('utf-8')
  print(q.strip())
  return q

# Hash a Rubik's Cube state with a given key using Blake2B
def hash(state, salt):
  salt = binascii.unhexlify(salt)
  state = state.encode('utf-8')
  return hashlib.blake2b(state, digest_size=16, key=salt).hexdigest()

if __name__ == '__main__':
  # First register an account with the name 'x' and with
  # public key as the null permutation
  recv()
  send('2')
  recv()
  send('x')
  recv()
  send(start)
  recv()
  send('3')
  recv()
  send('x')
  q = recv()
  their_pubkey = q[q.index('is:\n')+4:q.index('is:\n')+4+54]
  salt = q[q.index('y, "')+4:q.index('y, "')+4+16]
  h = hash(their_pubkey, salt)
  send(h)
  recv()

  # Once logged in, list all the users and record the admin's public key
  send('4')
  q = recv()
  admin_pubkey = q[q.index('Username: admin\nKey: ')+21:q.index('Username: admin\nKey: ')+21+54]

  # Next, try to login as admin
  send('3')
  recv()
  send('admin')
  q = recv()
  their_pubkey = q[q.index('is:\n')+4:q.index('is:\n')+4+54]
  salt = q[q.index('y, "')+4:q.index('y, "')+4+16]

  # Execute the MiTM attack on the service's public key to decompose it into
  # a * A_op + b * B_op
  (a, b) = MITM_ATTACK(their_pubkey)[0]

  # Compute the state after a * A_op, admin_pubkey, then b * B_op
  a1 = A_op(start, a)
  a2 = compose(a1, admin_pubkey)
  a3 = B_op(a2, b)

  # Hash the state and sent it to login
  h = hash(a3, salt)
  send(h)
  recv()
