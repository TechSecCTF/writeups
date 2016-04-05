#Toil33t

We are given a [web interface](http://toil33t.quals.nuitduhack.com) which lets us log in using a username, password, and email. Once we login, we are provided with a cookie such as

```
939c4dcbc5c09d3aaa00469fc65bbd6b5d998eabd9fd50d71639ffd19fadaeb23164706a5409b80800d7b98a576d11546cb3b01c5a57390325c7f6a18a4183c2e601b92d49560ffcac94c6271400069e
```

which presumably is our encrypted session information.

By digging into the source we can find `/session` which decrypts our cookie and reveals its contents:

```
{
  "email": "test@example.com",
  "is_admin": false,
  "show_ad": false,
  "username": "test"
}
```

Our goal is to set `is_admin` to true so that we can access the admin interface. The homepage states that the site uses "Rijndael + 256ROT13." Assuming that the latter part is a joke, we know that they're probably using AES (a block cipher) to encrypt the session state.

Our first step is to discover what block cipher [mode of operation](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation) they are using. To do this, we can register an account with the username consisting of multiple blocks of A's:

```
{
  "email": "",
  "is_admin": false,
  "show_ad": false,
  "username": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
}
```

Our encrypted cookie (when divided up into 16 byte blocks) looks like:

```
939c4dcbc5c09d3aaa00469fc65bbd6b
1cc38f6fb5e9dee5ec287a3a83bc0b39
1cc38f6fb5e9dee5ec287a3a83bc0b39
1cc38f6fb5e9dee5ec287a3a83bc0b39
1cc38f6fb5e9dee5ec287a3a83bc0b39
2c0fcba79ce825e7a3914b57b6c98395
169b614fe3c354939c88a77560d746d2
b456365d12077dfa8d128e9ce19ed415
ce6a85d2a10b531cac21853e01224a6e
```

Note that the 2nd through 5th blocks are all identical; this implies that they are using [ECB](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#ECB) mode, which means that we should be able to use a [cut-and-paste](http://cryptopals.com/sets/2/challenges/13/) attack to replace that `false` with `true`.

To do this, we need to figure out more information about the exact string being encrypted. Let's begin by computing how long the string is.

When all the fields are set to empty, the cookie is 5 blocks long which corresponds to eighty bytes. Because the string needs to be padded to a multiple of the block size, this tell us that the string is between 64 and 80 characters long. As we increase the length of our username, the number of blocks stays the same, until we hit a username of length 15, at which point we get 6 blocks.

The string, then, must be 80 - 14 = 66 bytes long. It turns out that if we remove the newlines and extraneous spaces from the output of `/session` we get a string with length exactly 66:

```
{"email": "", "is_admin": false, "show_ad": false, "username": ""}
```

However, the fields could be stored in a different order, since this doesn't change the length. Indeed, by changing the lengths of the email field and the username field independently, we can learn that the username field actually occurs before the email. We don't know about the relative ordering of `is_admin` and `show_ad` but lets assume for now that `show_ad` appears before `is_admin`:

```
{"username": "", "show_ad": false, "is_admin": false, "email": ""}
```

We'd like to construct the string:

```
{"username": "", "show_ad": false, "is_admin": true, "email": ""}
```
but this will be difficult because the block that includes `true` includes double quotes, which are quoted-out when included in the username or the email:

```
{
  "email": "test\"quotes",
  "is_admin": false,
  "show_ad": false,
  "username": "test\"quotes"
}
```

To get around this, we can include enough spaces (shown using underscores) before `true` such that it ends up in its own block:

```
{"username": "", "show_ad": false, "is_admin":____________true, "email": ""}
```

Since JSON doesn't care about extra spaces, this will decode to the same resulting object. Other solutions that we tried all resulted in JSON-decoding errors:

```
{
  "error": "Invalid JSON data !"
}
```

We also need to include enough A's in the username field to make sure that a block boundary occurs right before the first space:

```
{"username": "AA", "show_ad": false, "is_admin":____________true, "email": ""}
```

Now the fourth block is the encryption of `____________true`, the first three blocks are the encryption of `{"username": "AA", "show_ad": false, "is_admin":`, and the last block is the encryption of `, "email": ""}` (plus any padding).

We can find each of these in the same way: use the characters we control in the `username` field to align these values at a block boundary. Specifically, our desired fourth block is the second ciphertext block of:

```
{"username": "AAA____________true", "show_ad": false, "is_admin": false, "email": ""}
```

Our desired first 3 blocks are the first three blocks of:


```
{"username": "AA", "show_ad": false, "is_admin": false, "email": ""}
```

and our desired ending block is the last block of:


```
{"username": "AAAAAAAAAAAA", "show_ad": false, "is_admin": false, "email": ""}
```

Putting them together our encrypted cookie is:

```
939c4dcbc5c09d3aaa00469fc65bbd6b5d998eabd9fd50d71639ffd19fadaeb23164706a5409b80800d7b98a576d1154d53da7ab898a957599c7490d8f98a955961336e7d0c9629f12536f127cbc1297
```

which yields

```
{
  "email": "",
  "is_admin": true,
  "show_ad": false,
  "username": "AA"
}
```

Going back to the homepage and clicking on the Admin Interface button reveals the flag to be `NDH{22cf96f723f08382606119fe574953b9}`.
