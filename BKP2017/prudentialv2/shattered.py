import requests
import hashlib


pdf1 = open("shattered-1.pdf", 'r').read()
pdf2 = open("shattered-2.pdf", 'r').read()

print hashlib.sha1(pdf1).hexdigest()
print hashlib.sha1(pdf2).hexdigest()

#
# print hashlib.sha1(m1).hexdigest()
# print hashlib.sha1(m2).hexdigest()

# r = requests.get("http://54.202.82.13/?" + "name=" + m1.decode('utf-8') + "&password=" + m2.decode('utf-8'))
r = requests.get("http://54.202.82.13/", params = {'name' : pdf1, 'password': pdf2})
print(r.text)
