Install Codes
=============

Converts install codes to link keys.

This is a rewrite compatible to Python3 (the original was written in Python2).

Usage:

    $ python3 install_code.py <install_code>

Enter <install_code> without spaces. E.g. instead of 1234 5678 9012 3456 7890 1234 5678 9012 3456 enter it in the above command as 123456789012345678901234567890123456.

To test the correctness of the result you can use the following code for validation:

83FE D340 7A93 9723 A5C6 39B2 6916 D505 C3B5

Enter it like this:
```
$ python3 install_code.py 83FED3407A939723A5C639B26916D505C3B5
Derived Link Key: 66b6900981e1ee3ca4206b6b861c02bb
```
