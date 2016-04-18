#the stuff

We are given a pcap with a lot of Bing searches about why cilantro tastes like soap. Opening the stream in Wireshark, we notice that there are some SMTP packets at the top, one of which mentions "the stuff".

If we right-click on an SMTP packet and click "Follow TCP Stream" we can read the entire email:

```
220 wren.wv.cc.cmu.edu Python SMTP proxy version 0.2
EHLO [192.168.120.138]
502 Error: command "EHLO" not implemented
HELO [192.168.120.138]
250 wren.wv.cc.cmu.edu
MAIL FROM:<jdoe@example.com>
250 Ok
RCPT TO:<jsmith@example.com>
250 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
Message-ID: <1460851088.7821.1.camel@ubuntu>
Subject: The Stuff
From: John Doe <jdoe@example.com>
To: jsmith@example.com
Date: Sat, 16 Apr 2016 16:58:08 -0700
Content-Type: multipart/mixed; boundary="=-zAAY+FBv9yZgwoZy4KHy"
X-Mailer: Evolution 3.10.4-0ubuntu2 
Mime-Version: 1.0


--=-zAAY+FBv9yZgwoZy4KHy
Content-Type: text/plain
Content-Transfer-Encoding: 7bit

Yo, I got the stuff.


--=-zAAY+FBv9yZgwoZy4KHy
Content-Type: application/zip; name="flag.zip"
Content-Disposition: attachment; filename="flag.zip"
Content-Transfer-Encoding: base64

UEsDBBQACQAIAHGBkEjDELQcOSoAAFk3AAAIABwAZmxhZy5qcGdVVAkAA6XGElfKxhJXdXgLAAEE
6AMAAAToAwAAcu3qNOrf/ikOGiuwzSTfpxNkjsV6RU5ygGcK3CdWBI5s486P2jSZZMCE1dsgcB5C
...
... <more stuff here>
...
Z1VUBQADpcYSV3V4CwABBOgDAAAE6AMAAFBLBQYAAAAAAQABAE4AAACLKgAAAAA=


--=-zAAY+FBv9yZgwoZy4KHy--

.
250 Ok
QUIT
221 Bye
```

The base-64 encoded text seems to be an attatchment called `file.zip`. Once we base-64 decode the string back to a zip file and try to open it, we realize that it is password-protected.

Going back to Wireshark, we use the fitler `smtp` to filter out non-SMTP packets. We then notice a second SMTP stream:

```
220 wren.wv.cc.cmu.edu Python SMTP proxy version 0.2
EHLO [192.168.120.138]
502 Error: command "EHLO" not implemented
HELO [192.168.120.138]
250 wren.wv.cc.cmu.edu
MAIL FROM:<jdoe@example.com>
250 Ok
RCPT TO:<jsmith@example.com>
250 Ok
DATA
354 End data with <CR><LF>.<CR><LF>
Message-ID: <1460851191.7821.2.camel@ubuntu>
Subject: Wait, hang on
From: John Doe <jdoe@example.com>
To: jsmith@example.com
Date: Sat, 16 Apr 2016 16:59:51 -0700
Content-Type: text/plain
X-Mailer: Evolution 3.10.4-0ubuntu2 
Mime-Version: 1.0
Content-Transfer-Encoding: 7bit

Yo, you'll need this too: super_password1


.
250 Ok
QUIT
221 Bye
```

The password for the zip is `super_password1`, and opening the zip yields the image:

![flag](https://github.com/TechSecCTF/writeups/blob/master/plaidctf2016/thestuff/flag.jpg)

The flag is: `PCTF{LOOK_MA_NO_SSL}`.
