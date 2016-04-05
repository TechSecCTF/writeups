#Trololo

Filter out all packets with the protocol RTP/RTSP/RTCP using the Wireshark filter `!rtp && !rtsp && !rtcp`. These are for some video stream that is not relevant to the malware. 

One of the remaining packets is a response for a GET request for `/content.enc`. The content of this packet seems to contain "encrypted" data. A lot of the bytes are the same value: `0xfd`. Furthermore, none of the bytes happen to be within ASCII range (they all have leading bit 1). This suggest that we should invert all the bits (same thing as xor-ing with `0xff`):

```
Python 2.7.10
>>> x = "0d0a0d0ac3c087..."
>>> import binascii
>>> y = binascii.unhexlify(x)
>>> print(''.join([chr(ord(a) ^ 0xff) for a in y]))
```

The result is the following XML document:

```
????<?xml version="1.0" encoding="utf-8" ?>
<configuration>
        <mailSettings>
            <smtp from="crypto@ndh2k16.com">
                <network host="hermes.ndh2k16.local" port="25"/>
            </smtp>
        </mailSettings>
        <NDHCrypto.Settings>
            <setting name="EXT_TO_ENCRYPT" serializeAs="String">
                <value>docx:doc:xls:xlsx:pdf:jpg:odt:ods:png:bmp:avi:mp4</value>
            </setting>
            <setting name="KEY" serializeAs="String">
                <value>AD784DA62D1DDBB19B7F0500A52DD15C0BD70F924A5EF7C3CEA134C428747AFB</value>
            </setting>
            <setting name="SUBJECT" serializeAs="String">
                <value>New infected</value>
            </setting>
            <setting name="IRC_SRV" serializeAs="String">
                <value>irc://irc.ndh2k16.com:6667</value> 
            </setting>
            <setting name="IRC_CHAN" serializeAs="String">
                <valude>#Crypt0NDH2K16</value>
            </setting>
            <setting name="IRC_CHANPASS" serializeAs="String">
                <value>orudeujieh6oonge4She</value>
            </setting>
        </NDHCrypto.Settings>
</configuration>
```

The password (and therefore the flag) is `orudeujieh6oonge4She`.