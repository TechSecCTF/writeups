a = 100
b = 99
c = 98
d = 97
e= 104
f= 103
g= 102
h= 101
i= 112
j= 111
k= 110
l= 109
m= 108
n= 107
o= 106
p= 105

assert abs(0 - 0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-123) + 0 == 623
assert abs(0 - 0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-2) + abs(p-236) + 0 == 780
assert abs(a-0) + abs(0 - 0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-134) + 0 == 635
assert abs(i-0) + abs(0 - 0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-3) + abs(p-6) + 0 == 748
assert abs(a-0) + abs(b-0) + abs(0 - 0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-144) + 0 == 646
assert abs(i-0) + abs(j-0) + abs(0 - 0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-2) + abs(p-228) + 0 == 774
assert abs(a-0) + abs(b-0) + abs(c-0) + abs(0 - 0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-153) + 0 == 656
assert abs(i-0) + abs(j-0) + abs(k-0) + abs(0 - 0) + abs(m-0) + abs(n-0) + abs(o-3) + abs(p-16) + 0 == 740
assert abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(0 - 0) + abs(f-0) + abs(g-2) + abs(h-169) + 0 == 665
assert abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(0 - 0) + abs(n-0) + abs(o-2) + abs(p-236) + 0 == 784
assert abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(0 - 0) + abs(g-2) + abs(h-184) + 0 == 681
assert abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(0 - 0) + abs(o-2) + abs(p-199) + 0 == 748
assert abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(0 - 3) + abs(h-9) + 0 == 696
assert abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(0 - 3) + abs(p-54) + 0 == 711
assert abs(a-34) + abs(b-15) + abs(c-2) + abs(d-200) + abs(e-131) + abs(f-251) + abs(g-224) + abs(0 - 131) + 0 == 777
assert abs(i-192) + abs(j-32) + abs(k-15) + abs(l-16) + abs(m-205) + abs(n-0) + abs(o-19) + abs(0 - 184) + 0 == 822
