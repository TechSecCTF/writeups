Multicast was one of the earliest challenges released. We were given two files: a sage program called `generate.sage` and a file with 20 large integers called `data.txt`. This was `generate.sage`:

```
nbits = 1024
e = 5
flag = open("flag.txt").read().strip()
assert len(flag) <= 64
m = Integer(int(flag.encode('hex'),16))
out = open("data.txt","w")

for i in range(e):
    while True:    
        p = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
        q = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
        ni = p*q
        phi = (p-1)*(q-1)
        if gcd(phi, e) == 1:
            break

    while True:
        ai = randint(1,ni-1)
        if gcd(ai, ni) == 1:
            break

    bi = randint(1,ni-1)
    mi = ai*m + bi
    ci = pow(mi, e, ni)
    out.write(str(ai)+'\n')
    out.write(str(bi)+'\n')
    out.write(str(ci)+'\n')
    out.write(str(ni)+'\n')
```

The attack ("Hastad's Broadcast Attack on linear padding") is described [here](https://en.wikipedia.org/wiki/Coppersmith%27s_attack#H.C3.A5stad.27s_broadcast_attack).

[Sage](http://www.sagemath.org/) makes this attack trivial to implement. It only required 22 lines of code:

```
import binascii

data = open('data.txt', 'r')
y = data.read().split()

y = [Integer(a) for a in y]
z = [(y[4*i + 0], y[4*i + 1], y[4*i + 2], y[4*i + 3]) for i in range(5)]

ns = [a[3] for a in z]
cs = [a[2] for a in z]
bs = [a[1] for a in z]
ass = [a[0] for a in z]

ts = [crt([int(i == j) for j in range(5)], ns) for i in range(5)]

P.<x> = PolynomialRing(Zmod(prod(ns)))
gs = [(ts[i] * ((ass[i] * x + bs[i])**5 - cs[i])) for i in range(5)]
g = sum(gs)
g = g.monic()
roots = g.small_roots()

print binascii.unhexlify(hex(int(roots[0]))[2:-1])
```

After running for about 5 seconds, our program gives us the flag:

```
[multicast]> /Applications/SageMath/sage exploit.sage
PCTF{L1ne4r_P4dd1ng_w0nt_s4ve_Y0u_fr0m_H4s7ad!}
```
