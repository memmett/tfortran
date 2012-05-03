"""TFortran transforms."""

import re

class Transform(object):


    def __init__(self):
        self.dim = None
        self.compress = True
        self.interleave = False
        self.row_major = True

        # basic transforms: one of <,{,[,(, then { some stuff }, then one of ),],},>
        self.bt = re.compile('(<|{|\(|\[){([^{}]+)}(\)|\]|}|>)')

        # do multi: do multi(i, j, k; nx, ny, nz) ... end do multi
        self.dm = re.compile('do\s+multi\(([^)]+)\)(.*?)end\s+do\s+multi', re.DOTALL)


    def auto_expand(self, dims):
        """Transform [ 'n' ] to [ 'n1', 'n2', 'n3' ]."""

        if len(dims) == 1:
            base = dims[0]
            return map(lambda x: base + str(x), range(1, self.dim+1))
        return dims


    def select(self, string):
        toks = string.split(';')
        return toks[self.dim-1]


    def concat(self, string):
        toks = string.split(';')
        return ''.join(toks[:self.dim])


    def do_multi(self, indexes, body):

        toks = indexes.split(';')
        ltoks = toks[0].split(',') # loop tokens
        rtoks = toks[1].split(',') # range tokens

        src = []
        for i in range(len(ltoks)):
            src.append('do %s = 1, %s' % (ltoks[i], rtoks[i]))
        src.append(body)
        for i in range(len(ltoks)):
            src.append('end do')

        return '\n'.join(src)


    def indexing(self, string, plain=False):
        toks = string.split(';')

        if len(toks) > 1:
            dims, comp = toks
            dims = dims.split(',')
            dims = self.auto_expand(dims)

            if comp == '.':
                comp = str(self.dim)

            if self.compress and self.dim == 1 and comp == '1':
                return "%s" % dims[0]

        else:
            dims = toks[0]
            comp = None
            dims = dims.split(',')
            dims = self.auto_expand(dims)

        idxs = list(dims[:self.dim])

        if not plain and self.row_major:
            idxs.reverse()

        if comp:
            if self.interleave:
                idxs.insert(0, comp)
            else:
                idxs.append(comp)

        return ', '.join(map(lambda x: str(x).strip(), idxs))


    def transform(self, cur):

        # first pass: curly brace transforms
        while True:
            m = self.bt.search(cur)
            if m:
                new = cur[:m.start(0)]
                
                if m.group(1) == '{':
                    new += self.indexing(m.group(2), plain=False)
                elif m.group(1) == '<':
                    new += self.indexing(m.group(2), plain=True)
                elif m.group(1) == '[':
                    new += self.concat(m.group(2))
                elif m.group(1) == '(':
                    new += self.select(m.group(2))

                new = new + cur[m.end(0):]
                cur = new
            else:
                break

        # second pass: do multi
        while True:
            m = self.dm.search(cur)
            if m:
                new = cur[:m.start(0)]
                new += self.do_multi(m.group(1), m.group(2))
                new = new + cur[m.end(0):]
                cur = new
            else:
                break

        return cur
