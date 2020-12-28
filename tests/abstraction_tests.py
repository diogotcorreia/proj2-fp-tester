# NOTE: Esta implementação de TAD foi criada de propósito para ser absurda,
#   copiar isto seria extremamente obvio e uma má decisão académica.
# A cópia do seguinte código pode levar ao chumbo na Unidade Curricular.

class Pos:

    def __init__(self, c, l):
        self._foo = c
        self._bar = l

    def foobar(self):
        return Pos(self._foo, self._bar)

    def bar(self, foo):
        return self._foo == foo._foo and self._bar == foo._bar


posicaoMocks = (
    lambda c, l: Pos(c, l),
    lambda p: p.foobar(),
    lambda p: p._foo,
    lambda p: p._bar,
    lambda p: isinstance(p, Pos),
    lambda p1, p2: type(p1) == type(p2) == Pos and p1.bar(p2),
    lambda p: ''.join([p._foo, p._bar])
)


class Piece:

    def __init__(self, s):
        self._foo = s

    def foo(self, bar):
        return self._foo == bar._foo


pecaMocks = (
    lambda s: Piece(s),
    lambda j: Piece(j._foo),
    lambda j: type(j) == Piece,
    lambda j1, j2: type(j1) == type(j2) == Piece and j1.foo(j2),
    lambda j: ''.join([chr(91), j._foo, chr(93)])
)
