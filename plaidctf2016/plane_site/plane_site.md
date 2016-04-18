#plane_site

As the name of the problem suggests, the flag is hidden in one of the RGB planes of the image. In this instance it was hidden in the red plane. We can extract the flag using Mathematica:

```
Binarize[ColorNegate[ColorSeparate[<image>][[1]]], 0]
```

which yields:

The flag is `{PCTF{3_many_s3cr3ts}`.
