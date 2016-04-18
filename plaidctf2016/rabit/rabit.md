#rabit

We are given the source for an implementation of the [Rabin Cryptosystem](https://en.wikipedia.org/wiki/Rabin_cryptosystem). The message and ciphertext space are the quadratic residues modulo N, a product of two [Blum primes](https://en.wikipedia.org/wiki/Blum_integer). Encryption is defined as c = m^2 (mod N), and decryption involves taking square roots modulo N, a problem which is known to be hard unless you know N's factorization. The public key is N, and the private key is (p, q) where p • q = N.

The source code also functions as a least-significant-bit oracle: given any ciphertext encrypted using the specified public key, the server will send you the least significant bit of the corresponding plaintext message. Like [RSA](http://crypto.stackexchange.com/questions/11053/rsa-least-significant-bit-oracle-attack), the Rabin Cryptosystem is multiplicatively homomorphic, which allows us to recover the message completely using the oracle.

The key is that if we know that c = m^2 (mod N), then we also know that 4c = (2m)^2 (mod N). In general, given the ciphertext corresponding to m, we can find the ciphertext corresponding to 2^d • m. 

If the LSB of 2m (mod N) is 1, we know that m > N/2, because N is odd, so 2m must have wrapped around the modulus. Conversely, if 2m (mod N) is even (LSB = 0), we know that m < N/2. 

Furthermore, given that 2m (mod N) is even and 4m (mod N) is even, we know that m < N/4. If instead 4m (mod N) were odd, then N/4 < m < N/2. We can make similar statements if 2m (mod N) were odd.

Thus, by querying the LSB's of 2^d • m (mod N) for d = 1, 2, 3 ..., we can use binary search to pin down the range of m until we've found it exactly.

There are a couple of details ommitted in the above explanation. First of all, to rate-limit requests, the server requires a proof-of-work from the client in the form of computing a SHA1 which ends in `ffffff`.

Second of all, it is not always the case that 2^d • m will be a quadratic residue if d is odd. Namely, if 2 is not a quadratic residue modulo N, then the square of 2^d • m will decrypt to -(2^d • m) instead of 2^d • m. Since this number will have the opposite parity, we have to flip the bit that we receive from the server. Luckily, in this case 2 was a QR modulo N, so this aside was not relevant.

We were given

```
N = 81546073902331759271984999004451939555402085006705656828495536906802924215055062358675944026785619015267809774867163668490714884157533291262435378747443005227619394842923633601610550982321457446416213545088054898767148483676379966942027388615616321652290989027944696127478611206798587697949222663092494873481
c = 16155172062598073107968676378352115117161436172814227581212799030353856989153650114500204987192715640325805773228721292633844470727274927681444727510153616642152298025005171599963912929571282929138074246451372957668797897908285264033088572552509959195673435645475880129067211859038705979011490574216118690919
```

The code in `rabit_stew.py` runs the exploit described above and finds

```
m = 220166400929873038171224043083387335590015857856801737690673866137676770212340840723519830846763519609829027969455172753108185495429082225311362629007220379727503139832528666787769813670043777657959040951708803510803718999186543066351821584477532976979527966653153472510938246069633772948114592599064638196
```

Converting this to hex and interpreting as a string yields:

```
>>> import binascii
>>> binascii.unhexlify(hex(m)[2:-1])
'PCTF{LSB_is_4ll_y0u_ne3d}\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf2\xf4'
```

Stripping away the padding yields the flag: `PCTF{LSB_is_4ll_y0u_ne3d}`.