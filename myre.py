import re
f = open('tests/test1.t.f90', 'r')
s = f.read()
f.close()

done = False
# while not done:
#     m = re.search('{{([^{}]+)}}', s)
#     if m:
#         n = s[:m.start(0)]
#         n += s[m.end(0):]
#         print m.group(0), m.group(1)
#         s = n
#     else:
#         done = True

while not done:
    m = re.search('\[{([^{}]+)}\]', s)
    if m:
        n = s[:m.start(0)]
        # print m.group(0), m.group(1)
        toks = m.group(1).split(';')
        dim = 1
        n += ''.join(toks[:dim])
        n += s[m.end(0):]

        s = n
    else:
        done = True

print s
