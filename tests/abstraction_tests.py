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

posicaoFnNames = ('cria_posicao', 'cria_copia_posicao', 'obter_pos_c',
                  'obter_pos_l', 'eh_posicao', 'posicoes_iguais', 'posicao_para_str',)


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

pecaFnNames = ('cria_peca', 'cria_copia_peca', 'eh_peca',
               'pecas_iguais', 'peca_para_str',)


class Board:

    def __init__(self, a1=Piece(' '), b1=Piece(' '), c1=Piece(' '), a2=Piece(' '), b2=Piece(' '), c2=Piece(' '), a3=Piece(' '), b3=Piece(' '), c3=Piece(' ')):
        self.a1, self.b1, self.c1, self.a2, self.b2, self.c2, self.a3, self.b3, self.c3 = a1, b1, c1, a2, b2, c2, a3, b3, c3

    def foo(self):
        return Board(self.a1, self.b1, self.c1, self.a2, self.b2, self.c2, self.a3, self.b3, self.c3)

    def bar(self, x):
        return getattr(self, x)

    def foobar(self, x):
        _bar = list()
        _x = ord(x) > 90
        for y in range(3):
            _bar.append(getattr(self, x + str(y + 1)
                                if _x else chr(97 + y) + x))
        return tuple(_bar)

    def barfoo(self, x, y):
        setattr(self, y, x)
        return self

    def _foo(self, x, y):
        _bar = getattr(self, x)
        self.barfoo(Piece(' '), x)
        self.barfoo(_bar, y)
        return self

    def _bar(self, x):
        def _x(y, z): return posicaoMocks[5](y, z)
        return _x(self.a1, x.a1) and _x(self.b1, x.b1) and _x(self.c1, x.c1) and _x(self.a2, x.a2) and _x(self.b2, x.b2) and _x(self.c2, x.c2) and _x(self.a3, x.a3) and _x(self.b3, x.b3) and _x(self.c3, x.c3)

    def _foobar(self):
        def _x(x): return pecaMocks[4](x)
        return "   a   b   c\n1 "+_x(self.a1)+"-"+_x(self.b1)+"-"+_x(self.c1)+"\n   | \\ | / |\n2 "+_x(self.a2)+"-"+_x(self.b2)+"-"+_x(self.c2)+"\n   | / | \\ |\n3 "+_x(self.a3)+"-"+_x(self.b3)+"-"+_x(self.c3)+""


def _foobar(x): Piece(' ') if x == 0 else Piece('X') if x == 1 else Piece('O')


tabMocks = (
    lambda: Board(),
    lambda x: x.foo(),
    lambda x, y: x.bar(posicaoMocks[6](y)),
    lambda x, y: x.foobar(y),
    lambda x, y, z: x.barfoo(y, posicaoMocks[6](z)),
    lambda x, y: x.barfoo(Piece(' '), posicaoMocks[6](y)),
    lambda x, y, z: x._foo(posicaoMocks[6](y), posicaoMocks[6](z)),
    lambda x: type(x) == Board,
    lambda x, y: pecaMocks[3](Piece(' '), x.bar(posicaoMocks[6](y))),
    lambda x, y: type(x) == type(y) == Board and x._bar(y),
    lambda x: x._foobar(),
    lambda x: Board(_foobar(x[0][0]), _foobar(x[0][1]), _foobar(x[0][2]), _foobar(x[1][0]), _foobar(
        x[1][1]), _foobar(x[1][2]), _foobar(x[2][0]), _foobar(x[2][1]), _foobar(x[2][2]))
)

tabFnNames = ('cria_tabuleiro', 'cria_copia_tabuleiro', 'obter_peca', 'obter_vetor', 'coloca_peca', 'remove_peca',
              'move_peca', 'eh_tabuleiro', 'eh_posicao_livre', 'tabuleiros_iguais', 'tabuleiro_para_str', 'tuplo_para_tabuleiro')
