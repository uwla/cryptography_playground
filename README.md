# CRYPTOGRAPHY PLAYGROUND

This repository contains some python scripts that implement some
cryptography algorithms.

This is for learning purposes; do not use it in production!

## USING SAGEMATH

Most scripts are in python, but there are also sage scripts.
Here are instructions for working specifically with sagemath.

First, install sagemath. Then, to use it within python (or sage itself):

```shell
sage --preparse <module>.sage     # will generate a file called <module>.sage.py
mv <module>.sage.py <module>.py   # rename the file to be importable
```

Now, you just have to import it as a normal python module

```python
import <module>
```

## LICENSE

MIT
