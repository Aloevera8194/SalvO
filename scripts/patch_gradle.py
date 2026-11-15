import re, sys
p = 'android/app/build.gradle'
s = open(p).read()
block = '''    signingConfigs {
        debug {
            storeFile file("../../debug.keystore")
            storePassword "android"
            keyAlias "androiddebugkey"
            keyPassword "android"
            storeType "pkcs12"
        }
    }
'''
assert re.search(r'^android \{', s, re.M), 'bloco android nao encontrado'
s = re.sub(r'^android \{\n', lambda m: 'android {\n' + block, s, count=1, flags=re.M)
if 'versionCode 1' in s:
    s = s.replace('versionCode 1', 'versionCode ' + sys.argv[1], 1)
open(p, 'w').write(s)
print('build.gradle ajustado')
