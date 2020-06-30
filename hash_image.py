#!/usr/bin/python3

import hashlib
import os
import sys
 
filepath = 'imageio-python37.zip' 
f = open(filepath, 'rb')
data = f.read()
f.close()
 
print('MD5 : ' + hashlib.md5(data).hexdigest())
print('SHA-1 : ' + hashlib.sha1(data).hexdigest())
print('SHA-256 : ' + hashlib.sha256(data).hexdigest())
print('File Size : ' + str(os.path.getsize(filepath)) + ' Byte')

