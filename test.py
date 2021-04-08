import os
import re

f = open("out.txt", "r")
strings = re.findall(r'192.168.\d{1,3}.\d{1,3}', f.read())
print(strings)