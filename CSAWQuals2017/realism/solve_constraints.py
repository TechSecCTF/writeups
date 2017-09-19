import sys
sys.path.append('z3/build/')
from z3 import *

x = Int('x')
y = Int('y')

def abs(x):
  return If(x >= 0,x,-x)

s = Solver()

a = Int('a')
b = Int('b')
c = Int('c')
d = Int('d')
e = Int('e')
f = Int('f')
g = Int('g')
h = Int('h')
i = Int('i')
j = Int('j')
k = Int('k')
l = Int('l')
m = Int('m')
n = Int('n')
o = Int('o')
p = Int('p')

s.add(abs(a-34) + abs(b-15) + abs(c-2) + abs(d-200) + abs(e-131) + abs(f-251) + abs(g-224) + abs(0-131) + 0 == 655)
s.add(abs(i-192) + abs(j-32) + abs(k-15) + abs(l-16) + abs(m-205) + abs(n-0) + abs(o-19) + abs(0-184) + 0 == 735)
s.add(abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(0-2) + abs(h-143) + 0 == 605)
s.add(abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(0-2) + abs(p-223) + 0 == 656)
s.add(abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(0-0) + abs(g-2) + abs(h-93) + 0 == 545)
s.add(abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(0-0) + abs(o-2) + abs(p-144) + 0 == 521)
s.add(abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(0-0) + abs(f-0) + abs(g-2) + abs(h-33) + 0 == 632)
s.add(abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(0-0) + abs(n-0) + abs(o-2) + abs(p-9) + 0 == 635)
s.add(abs(a-0) + abs(b-0) + abs(c-0) + abs(0-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-120) + 0 == 563)
s.add(abs(i-0) + abs(j-0) + abs(k-0) + abs(0-0) + abs(m-0) + abs(n-0) + abs(o-2) + abs(p-123) + 0 == 505)
s.add(abs(a-0) + abs(b-0) + abs(0-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-51) + 0 == 657)
s.add(abs(i-0) + abs(j-0) + abs(0-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-1) + abs(p-249) + 0 == 606)
s.add(abs(a-0) + abs(0-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-145) + 0 == 597)
s.add(abs(i-0) + abs(0-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-2) + abs(p-94) + 0 == 553)
s.add(abs(0-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-85) + 0 == 624)
s.add(abs(0-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-2) + abs(p-41) + 0 == 529)

# s.add(abs(0 - 0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-123) + 0 == 623)
# s.add(abs(0 - 0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-2) + abs(p-236) + 0 == 780)
# s.add(abs(a-0) + abs(0 - 0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-134) + 0 == 635)
# s.add(abs(i-0) + abs(0 - 0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-3) + abs(p-6) + 0 == 748)
# s.add(abs(a-0) + abs(b-0) + abs(0 - 0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-144) + 0 == 646)
# s.add(abs(i-0) + abs(j-0) + abs(0 - 0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-2) + abs(p-228) + 0 == 774)
# s.add(abs(a-0) + abs(b-0) + abs(c-0) + abs(0 - 0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-153) + 0 == 656)
# s.add(abs(i-0) + abs(j-0) + abs(k-0) + abs(0 - 0) + abs(m-0) + abs(n-0) + abs(o-3) + abs(p-16) + 0 == 740)
# s.add(abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(0 - 0) + abs(f-0) + abs(g-2) + abs(h-169) + 0 == 665)
# s.add(abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(0 - 0) + abs(n-0) + abs(o-2) + abs(p-236) + 0 == 784)
# s.add(abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(0 - 0) + abs(g-2) + abs(h-184) + 0 == 681)
# s.add(abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(0 - 0) + abs(o-2) + abs(p-199) + 0 == 748)
# s.add(abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(0 - 3) + abs(h-9) + 0 == 696)
# s.add(abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(0 - 3) + abs(p-54) + 0 == 711)
# s.add(abs(a-34) + abs(b-15) + abs(c-2) + abs(d-200) + abs(e-131) + abs(f-251) + abs(g-224) + abs(0 - 131) + 0 == 777)
# s.add(abs(i-192) + abs(j-32) + abs(k-15) + abs(l-16) + abs(m-205) + abs(n-0) + abs(o-19) + abs(0 - 184) + 0 == 822)

s.add(a >= 32)
s.add(b >= 32)
s.add(c >= 32)
s.add(d >= 32)
s.add(e >= 32)
s.add(f >= 32)
s.add(g >= 32)
s.add(h >= 32)
s.add(i >= 32)
s.add(j >= 32)
s.add(k >= 32)
s.add(l >= 32)
s.add(m >= 32)
s.add(n >= 32)
s.add(o >= 32)
s.add(p >= 32)

s.add(127 > a)
s.add(127 > b)
s.add(127 > c)
s.add(127 > d)
s.add(127 > e)
s.add(127 > f)
s.add(127 > g)
s.add(127 > h)
s.add(127 > i)
s.add(127 > j)
s.add(127 > k)
s.add(127 > l)
s.add(127 > m)
s.add(127 > n)
s.add(127 > o)
s.add(127 > p)

print(s.check())
mod = s.model()


chars = [mod[a],
mod[b],
mod[c],
mod[d],
mod[e],
mod[f],
mod[g],
mod[h],
mod[i],
mod[j],
mod[k],
mod[l],
mod[m],
mod[n],
mod[o],
mod[p]]


print chars
flag = ''.join([chr(int(str(w))) for w in chars])
flag = flag[::-1]
print('flag' + flag[12:] + flag[8:12] + flag[0:4] + flag[4:8])
