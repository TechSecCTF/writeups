# CSAW CTF 2017 - Realism (400 pts)


This problem was much like any other CTF reversing challenge, but instead of a Linux or Windows executable, the binary was a [Master Boot Record](https://en.wikipedia.org/wiki/Master_boot_record) (MBR) that needed to be run under the [QEMU](https://www.qemu.org/) full-system emulator.

We're given the command to boot the MBR, `qemu-system-i386 -drive format=raw,file=realism`, and we're presented with this:

![hello](https://i.imgur.com/W9BxK6O.png)

Simple, right? The entire MBR is only 512 bytes in size, so it's not much to reverse.

# Static Analysis
First, we load the MBR into [IDA](https://www.hex-rays.com/products/ida/), and after some tinkering, realize it gives a nice disassembly in 16-bit mode.

From any OS class, we should know that the MBR is loaded at physical address `0x7c00`, but it's not hard to tell from all the references to `loc_7C__`. We can re-load the binary in IDA at offset `0x7c00`, giving us nice, clickable references. Here's the [full disassembly](https://github.com/TechSecCTF/writeups/blob/master/CSAWQuals2017/realism/realism.ida), with some strings commented.

The important part of the MBR, the flag-checking bit, begins at `0x7C6F`:

```
seg000:7C66                 cmp     ds:byte_7DC8, 13h
seg000:7C6B                 jle     loc_7D0D
seg000:7C6F                 cmp     dword ptr ds:1234h, 'galf'
seg000:7C78                 jnz     loc_7D4D
seg000:7C7C                 movaps  xmm0, xmmword ptr ds:1238h
seg000:7C81                 movaps  xmm5, xmmword ptr ds:loc_7C00
seg000:7C86                 pshufd  xmm0, xmm0, 1Eh
seg000:7C8B                 mov     si, 8
seg000:7C8E
seg000:7C8E loc_7C8E:                               ; CODE XREF: seg000:7CC1j
seg000:7C8E                 movaps  xmm2, xmm0
seg000:7C91                 andps   xmm2, xmmword ptr [si+7D90h]
seg000:7C96                 psadbw  xmm5, xmm2
seg000:7C9A                 movaps  xmmword ptr ds:1268h, xmm5
seg000:7C9F                 mov     di, ds:1268h
seg000:7CA3                 shl     edi, 10h
seg000:7CA7                 mov     di, ds:1270h
seg000:7CAB                 mov     dx, si
seg000:7CAD                 dec     dx
seg000:7CAE                 add     dx, dx
seg000:7CB0                 add     dx, dx
seg000:7CB2                 cmp     edi, [edx+7DA8h]
seg000:7CBA                 jnz     loc_7D4D
seg000:7CBE                 dec     si
seg000:7CBF                 test    si, si
seg000:7CC1                 jnz     short loc_7C8E
```

First, it compares a DWORD at physical address `0x1234` (where the input is read into), with `"flag"`, and if they're equal, carries out a series of floating-point operations on [XMM registers](https://en.wikipedia.org/wiki/Streaming_SIMD_Extensions).

Basically, the rest of this assembly snippet will loop through the input bytes, perform XMM operations on each one, and compare the result against a [sequence of bytes](https://github.com/TechSecCTF/writeups/blob/70fedf363d08acc7c5b9bf3d3d5c1ef53dce0636/CSAWQuals2017/realism/realism.ida#L201) at
the end of the boot record. The key to this problem is understanding the XMM operations.

The XMM registers are 128-bits long and are normally used for fast floating point operations. In this challenge they're being (ab)used for obfuscating the flag.

# Dynamic Analysis
You can attach a gdb instance to QEMU by adding a `-s` option, and then connecting with

```
gdb -ex 'target remote localhost:1234' \
    -ex 'set architecture i8086' \
    -ex 'break *0x7c6f' \
    -ex 'continue'
```

If we input a string that starts with `"flag"`, passing the first `cmp`, we can see the initial value in `xmm0` when it starts the checking loop at `loc_7c8e`.

We can actually print these XMM registers in GDB.`xmm0` is initially the 16 bytes of our input that follow `flag` — we can test it with `abcdefghijklmnop`.


```
(gdb) p $xmm0
$3 = {..., uint128 = 0x706f6e6d6c6b6a696867666564636261}
```


`xmm5` is loaded with the bytes at the beginning of the MBR:

```
(gdb) p $xmm5
$2 = {..., uint128 = 0x220f02c883fbe083c0200f10cd0013b8}
```

The`pshufd` [instruction](http://x86.renejeschke.de/html/file_module_x86_id_254.html) shuffles our input in a manner determined by the argument `0x1E`, resulting in
```
(gdb) p $xmm0
$4 = {..., uint128 = 0x6463626168676665706f6e6d6c6b6a69}
```
Next, a loop that checks each byte of this shuffled input. Let's break down what it does:

1. Applies a [mask](https://github.com/TechSecCTF/writeups/blob/70fedf363d08acc7c5b9bf3d3d5c1ef53dce0636/CSAWQuals2017/realism/realism.ida#L177) to the input (`0x7c91`)
2. Computes a "[sum of absolute differences"](http://www.felixcloutier.com/x86/PSADBW.html) between `xmm5` (initialized to some constant data) and `xmm2` (which stores our masked input), updating `xmm5`  (`0x7c96`)
3. Moves the upper and lower portions of the result into EDI (`0x7c9a-0x7ca7`)
5. Compares EDI with some value in the MBR (`0x7cb2`)
6. Decrements the counter and loops back if there are more bytes to check

This loop runs for 8 iterations before exiting and displaying the "CORRECT" message. So, once we've fully reversed this snippet, the goal is to find the flag that passes these checks.

# SMT Solving
Let's treat each byte of the input we pass in as a separate variable, $a$ through $p$. Because of the nature of the `psadbw` instruction from step 2, each iteration of the loop gives us two equations involving our variables. This results in $8 \cdot 2 = 16$ equations among $16$ variables.

Since the equations involve absolute values, they're non-linear, but that should be no problem for any [SMT solver](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories) worth its salt. We'll use [Z3](https://github.com/Z3Prover/z3), a powerful theorem-prover developed by Microsoft. Our strategy will be to write some python code to generate our equations, and then pass these equations to Z3 to find a solution.

Our python code will have to simulate the operations performed by the XMM instructions. We'll ignore the shuffle instruction for now, since that is only performed once before the loop. This is the core function of [the script](https://github.com/TechSecCTF/writeups/blob/master/CSAWQuals2017/realism/print_constraints.py) we wrote:

```python
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
```

When run, it outputs our 16 equations:

```
abs(a-34) + abs(b-15) + abs(c-2) + abs(d-200) + abs(e-131) + abs(f-251) + abs(g-224) + abs(0-131) + 0 == 655,
abs(i-192) + abs(j-32) + abs(k-15) + abs(l-16) + abs(m-205) + abs(n-0) + abs(o-19) + abs(0-184) + 0 == 735,
abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(0-2) + abs(h-143) + 0 == 605,
abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(0-2) + abs(p-223) + 0 == 656,
abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(0-0) + abs(g-2) + abs(h-93) + 0 == 545,
abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(0-0) + abs(o-2) + abs(p-144) + 0 == 521,
abs(a-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(0-0) + abs(f-0) + abs(g-2) + abs(h-33) + 0 == 632,
abs(i-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(0-0) + abs(n-0) + abs(o-2) + abs(p-9) + 0 == 635,
abs(a-0) + abs(b-0) + abs(c-0) + abs(0-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-120) + 0 == 563,
abs(i-0) + abs(j-0) + abs(k-0) + abs(0-0) + abs(m-0) + abs(n-0) + abs(o-2) + abs(p-123) + 0 == 505,
abs(a-0) + abs(b-0) + abs(0-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-51) + 0 == 657,
abs(i-0) + abs(j-0) + abs(0-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-1) + abs(p-249) + 0 == 606,
abs(a-0) + abs(0-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-145) + 0 == 597,
abs(i-0) + abs(0-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-2) + abs(p-94) + 0 == 553,
abs(0-0) + abs(b-0) + abs(c-0) + abs(d-0) + abs(e-0) + abs(f-0) + abs(g-2) + abs(h-85) + 0 == 624,
abs(0-0) + abs(j-0) + abs(k-0) + abs(l-0) + abs(m-0) + abs(n-0) + abs(o-2) + abs(p-41) + 0 == 529,
```

We can now take these equations and add each of them to Z3 as a constraint. To do this, we'll first define a solver `s`, declare 16 integer variables, and constrain each of them to be printable ASCII values. We also need to define [our own absolute value function](https://stackoverflow.com/questions/22547988/how-to-calculate-absolute-value-in-z3-or-z3py) that Z3 can use.

```python
import sys
sys.path.append('z3/build/')
from z3 import *

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
```

Then, we'll add our 16 equations:

```python
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
```

And finally, we'll ask Z3 to extract a solution, and reshuffle our variables to obtain the flag:

```python
print(s.check())
mod = s.model()

chars = [
          mod[a],
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
          mod[p]
        ]


print chars
flag = ''.join([chr(int(str(w))) for w in chars])
flag = flag[::-1]
print('flag' + flag[12:] + flag[8:12] + flag[0:4] + flag[4:8])
```

```
[realism]> python solve_constraints.py
sat
[51, 114, 52, 123, 95, 122, 108, 97, 125, 48, 121, 95, 51, 100, 48, 109]
flag{4r3alz_m0d3_y0}
```

Entering the flag in QEMU confirms that it's correct:

![](https://i.imgur.com/v0O5BVe.png)
