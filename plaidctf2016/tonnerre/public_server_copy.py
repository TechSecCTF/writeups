#/usr/bin/env python

from Crypto.Random import random, atfork
from Crypto.Hash import SHA256

msg = """Welcome to the Tonnerre Authentication System!\n"""
flag = "REDACTED"

N = 168875487862812718103814022843977235420637243601057780595044400667893046269140421123766817420546087076238158376401194506102667350322281734359552897112157094231977097740554793824701009850244904160300597684567190792283984299743604213533036681794114720417437224509607536413793425411636411563321303444740798477587L
g = 9797766621314684873895700802803279209044463565243731922466831101232640732633100491228823617617764419367505179450247842283955649007454149170085442756585554871624752266571753841250508572690789992495054848L

permitted_users = {'get_flag': (0xd14058efb3f49bd1f1c68de447393855e004103d432fa61849f0e5262d0d9e8663c0dfcb877d40ea6de6b78efd064bdd02f6555a90d92a8a5c76b28b9a785fd861348af8a7014f4497a5de5d0d703a24ff9ec9b5c1ff8051e3825a0fc8a433296d31cf0bd5d21b09c8cd7e658f2272744b4d2fb63d4bccff8f921932a2e81813L, 165674960298677315369642561867883496091624769292792204074150337092614964752287803122621876963359715780971900093578962850132496591192295131510624917204670192364009271723089444839548606533268832368676268405764377988005323809734321470184299186127132537376393324213965008025487569799622831466701444653263068925529L)}

# This should import the fields from the data into the dictionary.
# the dictionary is indexed by username, and the data it contains are tuples
# of (salt, verifier) as numbers. note that the database stores these in hex.
#import_permitted_users(permitted_users)

def H(P):
  h = SHA256.new()
  h.update(P)
  return h.hexdigest()

def tostr(A):
  return hex(A)[2:].strip('L')

def handle():
  print(msg)
  username = raw_input("").strip('\n')
  if username not in permitted_users:
    print('Sorry, not permitted.\n')
    return
  public_client = int(raw_input("").strip('\n'), 16) % N
  c = (public_client * permitted_users[username][1]) % N
  if c in [N-g, N-1, 0, 1, g]:
    print('Sorry, not permitted.\n')
    return
  random_server = random.randint(2, N-3)
  public_server = pow(g, random_server, N)
  residue = (public_server + permitted_users[username][1]) % N
  print(tostr(permitted_users[username][0]) + '\n')
  print(tostr(residue) + '\n')

  session_secret = (public_client * permitted_users[username][1]) % N

  assert pow(g, 2, N) == session_secret

  session_secret = pow(session_secret, random_server, N)
  session_key = H(tostr(session_secret))

  proof = raw_input("").strip('\n')

  if (proof != H(tostr(residue) + session_key)):
    print('Sorry, not permitted.\n')
    return

  our_verifier = H(tostr(public_client) + session_key)
  print(our_verifier + '\n')

  print('Congratulations! The flag is ' + flag + '\n')
  return

if __name__ == '__main__':
  handle()
