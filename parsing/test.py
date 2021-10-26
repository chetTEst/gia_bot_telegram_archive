# -*- coding: utf-8 -*-
f=open('123.txt','r')
result=f.read()
print(result.encode('ascii', 'backslashreplace'))
f.close()