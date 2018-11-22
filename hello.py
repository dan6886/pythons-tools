import re

a = '[  0%] /data/local/tmp/dance_1.0_2018-04-17.APK'
ret = re.search('[0-9]*%', a)
print(ret.group())
