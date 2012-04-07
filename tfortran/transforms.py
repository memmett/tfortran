"""TFortran transforms."""

from pyparsing import *


class BaseTransform(object):

    def __init__(self):
        self._dim = None
        self.parser.setParseAction(self.action)

    @property
    def dim(self):
        if self._dim:
            return self._dim
        raise ValueError('dimension not set')

    @dim.setter
    def dim(self, value):
        self._dim = value

    def __call__(self, string):
        return self.parser.transformString(string)

    def action(self, src, loc, toks):
        raise NotImplementedError


class Indexing(BaseTransform):

    parser = nestedExpr('{{', '}}', Regex(r"[^{}]+"))

    def __init__(self):
        super(Indexing, self).__init__()
        self.compress   = True
        self.interleave = True
        self.row_major  = False


    def auto_expand(self, dims):
        if len(dims) == 1:
            base = dims[0]
            return map(lambda x: base + str(x), range(1, self.dim+1))
        return dims


    def action(self, src, loc, toks):
        toks = toks[0][0].split(';')

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
        if comp:
            if self.interleave:
                idxs.insert(0, comp)
            else:
                idx.append(comp)

        if self.row_major:
            idxs.reverse()

        return ', '.join(map(lambda x: str(x).strip(), idxs))


class Select(BaseTransform):

    parser = nestedExpr('({', '})', delimitedList(Regex(r"[^{};]+"), ';'))

    def action(self, src, loc, toks):
        return toks[0][self.dim-1]


class Concat(BaseTransform):

    parser = nestedExpr('[{', '}]', delimitedList(Regex(r"[^{};]+"), ';'))

    def action(self, src, loc, toks):
        return ' '.join(toks[0][:self.dim])


class DoMulti(BaseTransform):

    parser = ( CaselessKeyword('do multi')
               + nestedExpr('(', ')',
                            delimitedList(Word(alphanums)) + ';'
                            + delimitedList(Word(alphanums)))
               + Regex(".*")
               + CaselessKeyword('end do multi') )

    def action(self, src, loc, toks):
        nloops = int((len(toks[1])-1)/2)
        ivars  = toks[1][:nloops]
        ranges = toks[1][nloops+1:]
        body   = toks[2]

        src = []
        for i in range(nloops):
            src.append('do %s = 1, %s' % (ivars[i], ranges[i]))
        src.append(body)
        for i in range(nloops):
            src.append('end do')

        return '\n'.join(src)


# order is important...
transforms = [
    Select(),
    Concat(),
    Indexing(),
    DoMulti(),
    ]
