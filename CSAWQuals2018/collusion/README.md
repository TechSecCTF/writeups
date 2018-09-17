# CSAW CTF 2018 Qualification Round - Collusion

Writeup by: Andrew He

## Challenge
Crypto, 500 pts, 32 solves

Written by Brendan McMillion, Cloudflare

### Files

* bobs-key.json
* carols-key.json
* common.go
* message.json
* generate-challenge.go

## tl;dr

We're given an RSA-based identity-based encryption (IBE) scheme, and two users'
private keys. Turns out those are enough to figure out the group manager's
private key, allowing us to decrypt arbitrary messages.

## Deciphering the crypto system

I jumped on this problem after [betaveros](https://beta.vero.site/) had already
read and simplified the code, so I got a bit of a condensed form of the problem:
we're given a large semiprime `N=pq`, integers `a`, `b`, `c`, `inv(x+b) mod
phi(N)`, `inv(x+c) mod phi(N)`, `3^(r*(x+a)) mod N`, and the flag encrypted with
`3^r mod N` as the key (here, `p`, `q`, `r`, and `x` are unknowns). I'll dive
into a little more detail where these came from, but feel free to jump to the
next section for the solution and exploit.

The go files contain an identity-based encryption scheme, which allows anyone to
encrypt data using just the recipient's name (you can think of it as a
public-key distribution system that magically uses a common public/private key
owned by a trusted third-party).

In this scheme, the trusted group manager first generates an RSA semi-prime `N =
p * q` using safe primes `p = 2p'+1` and `q = 2q'+1`, as well as a secret value
`x` modulo `phi(N)`. They publish `N` and `H = 3^x` as public keys. Also,
there's a public function `DecrypterId` maps the identity (name) of the
recipient to a deterministic integer modulo `N`.

For any recipient with `DecrypterId(recipient) = id`, the group manager
distributes `N` and `d = inv(x + id) mod phi(N)` as their private decryption
key (presumably after properly verifying their identity).

To encrypt for a recipient with `DecrypterId(recipient) = id`, we first pick a
shared secret `K = 3^r mod N` for a random `r`, and then produce the
key-encapsulation message (KEM) `V = (3^id * H)^r mod N = 3^(r*(x + id)) mod N`.
The secret secret is used to encrypt the message with an AES cipher and a random
nonce plugged into Go's AEAD black box, and we send the triple `(V, AEAD(...),
nonce)`.

To decrypt, the recipient can recover the shared secret by taking

    V^d mod N = 3^(r*(x+id))^(inv(x+id) mod phi(N)) mod N = 3^r mod N

as in standard RSA.

In this problem, we're given Bob and Carols' secret keys, as well as an
encrypted message for Alice containing the flag. From these, we can find:
* `N` from the secret keys,
* `a`, `b`, and `c`, the `DecrypterId`s of Alice, Bob, and Carol,
* `inv(x+b) mod phi(N)` and `inv(x+c) mod phi(N)`, the secret keys of Bob and Carol,
* `3^(r*(x+a)) mod N`, the KEM of the message
* the message ciphertext and nonce itself

Interestingly, we weren't given the public encryption key, even though the
challenge program supposedly saves it. We didn't need it in the end, but just a
small oddity.

## Some number theory

The number theory part of this challenge was pretty short and sweet once we saw
it.

In essence, we know `1/(x+b) mod phi(N)` and `1/(x+c) mod phi(N)` for given
`b` and `c`, so we'd like to find some information about `x` or `phi(N)` or
both. We can't take modular inverses because `phi(N)` is unknown, so the next
best thing is maybe working directly with the fractions.

A bit of experimentation led us to the identity

    1/(x+b) - 1/(x+c) = (c-b) / (x+b) / (x+c) mod phi(N)

Note that we can compute the left hand side and right hand side of this
equation, so subtracting gives us a multiple of `phi(N)`. If we let this
multiple be `myPhi`, we can do our modular arithmetic modulo `myPhi`, and it
will be correct mod `phi(N)`!

In particular, we can just compute `x+b = inv(inv(x+b) mod phi) mod myPhi`,
which allows us to find `x`, `x+a`, and `inv(x+a) mod myPhi`. Then, we can just
use `inv(x+a) mod myPhi` as Alice's decryption key to decrypt the flag, as it's
congruent to `inv(x+a) mod phi(N)`.

One small note: it's possible that the numbers we work with aren't relatively
prime with `myPhi`, in which case we can't take modular inverses. However, we
know that `x+b` and `x+a` are both relatively prime with `phi(N)`, so the common
factors with `myPhi` must be extraneous, so we can just divide them out of
`myPhi`. Fortunately, this didn't occur in the actual challenge data, so we
didn't have to implement this.

## Exploit

The exploit can be found in `exploit.go` and can be built with `go build
exploit.go common.go`. One weird point was having to implement `Decrypt`
ourselves: the given code implemented `Encrypt` but not the matching function.
