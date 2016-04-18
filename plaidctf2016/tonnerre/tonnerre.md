# tonnerre
There are two phases to this problem: a SQL injection to recover some data, and an attack on [SRPv1](https://en.wikipedia.org/wiki/Secure_Remote_Password_protocol) that relies on the recovered data.

## SQL Injection
We are given a [website](http://tonnerre.pwning.xxx:8560/) with a username and password login form. Initial tests confirm that both fields are injectible. We'll let [sqlmap](sqlmap.org) do all the heavy lifting:

```
python sqlmap.py -u "http://tonnerre.pwning.xxx:8560/login.php" --method POST --data "username=asdjf&password=asdjf" -p "username" --dump
```

sqlmap then dumps the contents of the database which consist of two tables. The first table `admin_users` contains just two columns:

```
pass                                |  user
------------------------------------+-------
adminpasswordbestpasswordmostsecure |  admin
```

We can use this password to login to the website, but we just get this message: 

> Authentication successful for user admin! However, administration is disabled right now due to ongoing hacking attempts. Check again later.

The second table, `users`, is more interesting. It too has only one row, with 3 columns corresponding to the salt, user, and verifier:

```
salt: d14058efb3f49bd1f1c68de447393855e004103d432fa61849f0e5262d0d9e8663c0dfcb877d40ea6de6b78efd064bdd02f6555a90d92a8a5c76b28b9a785fd861348af8a7014f4497a5de5d0d703a24ff9ec9b5c1ff8051e3825a0fc8a433296d31cf0bd5d21b09c8cd7e658f2272744b4d2fb63d4bccff8f921932a2e81813
user: get_flag
verifier: ebedd14b5bf7d5fd88eebb057af43803b6f88e42f7ce2a4445fdbbe69a9ad7e7a76b7df4a4e79cefd61ea0c4f426c0261acf5becb5f79cdf916d684667b6b0940b4ac2f885590648fbf2d107707acb38382a95bea9a89fb943a5c1ef6e6d064084f8225eb323f668e2c3174ab7b1dbfce831507b33e413b56a41528b1c850e59
```
We'll need this data for the second part.

## SRP Exploit
Secure Remote Password is a protocol that uses a zero knowledge proof to authenticate to a server without the server learning any details about your password. Here's a sketch of the protocol:

* The Client (C) and the Server (S) agree on N, a safe prime, and g, a generator in Z_N.
* C generates a random salt and picks a password and computes x = SHA256(salt || password), and v = g^x (mod N).
* Upon registration to the site, C sends the salt and password to S, which also computes x and v, but then throws the password and x away, keeping only the salt and v.
* Upon logging in, C picks a random a in Z_N and computes A = g^a (mod N), sending this to S.
* S picks a random b in Z_N, and computes and sends B = v + g^b (mod N) to C.
* C computes k = (B - v)^(a + x) = g^(ax + bx) (mod N)
* S computes k = (Av)^b = g^(ax + bx) (mod N)
* C sends SHA256(k) to S, and S allows C to log in if this matches S's own computation.

That's a lot of math, but the key to the protocol is that the server and client both manage to compute g^(ax + bx) despite neither of them ever sending a, x, or b in the clear. Note that v is known as the verifier, and is equal to the value that we found at the end of the first part.

The exploit is suggested by a certain line present in the server-side code:

```
if c in [N-g, N-1, 0, 1, g]:
	req.sendall('Sorry, not permitted.\n')
	req.close()
	return
```

At this point in the code, c = Av = g^(a + x). What would go wrong if c = 0? Suppose that a malicious user sends A = 0 in the protocol. Then the user knows that the shared secret k = (Av)^b = 0, so the user would be able to successfully authenticate without knowing the password.

What would go wrong if c = g? This would mean that a = -x + 1, which means that A = g^(-x + 1) = g • v^(-1). In this case the shared secret is k = (Av)^b = g^b, which the malicious user can calculate as B - v. 

Both of these attacks are prevented by the code above, but it's presence suggests another attack. What would go wrong if c = g^2? This would mean that a = -x + 2, which means that A = g^(-x + 2) = g^2 • v^(-1). In this case the shared secret is k = (Av)^b = g^(2b), which the malicious user can calculate as (B - v)^2.

In summary, the exploit is as follows:

* Malicious user (M) obtains v somehow
* M calculates A = g • v^(-1) (mod N) and sends this to S.
* S sends back B
* M calculates k = (B - v)^2, and sends SHA256(k) to S.
* S accepts this as valid and lets M log in (or in our case, sends back the flag).

The exploit is implemented in `srp_exploit.py`. 

Note that this attack only works if the malicious user knows v, the verifier. In this case, we happen to know v because of a database leak. However, since database leaks are [surprisingly common](http://arstechnica.com/gaming/2012/08/hackers-collect-significant-account-details-from-blizzard-servers/), later versions of SRP corrected this vulnerability.

The flag is `PCTF{SrP_v1_BeSt_sRp_c0nf1rm3d}`.
