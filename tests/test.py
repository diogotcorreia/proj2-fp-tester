import unittest
from unittest.mock import patch
import sys
import importlib
import os
from io import StringIO

target = importlib.import_module(sys.argv[1])


class TestTADPosicao(unittest.TestCase):

    def setUp(self):
        self.positions = tuple((x, y) for x in 'abc' for y in '123')

    def test_cria_posicao_fail(self):
        """
        Testa a verificação dos argumentos.
        Todos os casos devem retornar ValueError.
        """
        testcases = (('a', '4'), ('d', '2'), (True, False),
                     ('c', 2), ('aa', '-2'), ('b', 3.0), ('c', '11'), ('ab', '12'))

        for case in testcases:
            with self.assertRaises(ValueError, msg='ValueError not raised for {}'.format(case)) as ctx:
                target.cria_posicao(case[0], case[1])
            self.assertEqual(
                'cria_posicao: argumentos invalidos', str(ctx.exception))

    def test_cria_posicao_success(self):
        """
        Testa a criação dos argumentos sem retornar ValueError.
        Todas as 9 posições possiveis são testadas.
        """
        for case in self.positions:
            try:
                target.cria_posicao(case[0], case[1])
            except ValueError:
                self.fail("cria_posicao raised ValueError when it shouldn't")

    def test_cria_copia_posicao(self):
        """
        Testa a criação de uma cópia de todas as posições possíveis.
        Relembra-se que a cópia não pode ser o mesmo objeto que o original,
        isto é, "original is copia" tem de retornar False.
        """
        for case in self.positions:
            original = target.cria_posicao(case[0], case[1])
            copy = target.cria_copia_posicao(original)
            self.assertIsNot(original, copy)
            self.assertTrue(target.posicoes_iguais(original, copy))

    def test_obter_pos_c(self):
        """
        Testa obter_pos_c para todas as posições possíveis
        """
        for case in self.positions:
            pos = target.cria_posicao(case[0], case[1])
            self.assertEqual(case[0], target.obter_pos_c(pos))

    def test_obter_pos_l(self):
        """
        Testa obter_pos_l para todas as posições possíveis
        """
        for case in self.positions:
            pos = target.cria_posicao(case[0], case[1])
            self.assertEqual(case[1], target.obter_pos_l(pos))

    def test_posicoes_iguais_success(self):
        """
        Testa posicoes_iguais para todas as posições válidas possíveis
        """
        for case in self.positions:
            pos1 = target.cria_posicao(case[0], case[1])
            pos2 = target.cria_posicao(case[0], case[1])
            self.assertTrue(target.posicoes_iguais(pos1, pos2))

    def test_posicoes_iguais_fail(self):
        """
        Testa posicoes_iguais para posições diferentes
        """
        pos1 = target.cria_posicao('a', '2')
        pos2 = target.cria_posicao('b', '3')
        self.assertFalse(target.posicoes_iguais(pos1, pos2))

    def test_eh_posicao_success(self):
        """
        Testa eh_posicao para todas as posições válidas possíveis
        """
        for case in self.positions:
            pos1 = target.cria_posicao(case[0], case[1])
            self.assertTrue(target.eh_posicao(pos1))

    def test_eh_posicao_fail(self):
        """
        Testa eh_posicao para objetos que não sejam posições
        """
        for case in (True, False, 34, 'fail', 43.543, {'c': 'a', 'l': 4}, ['z', '4'], ('d', '1'), {'coluna': 'b', 'linha': '12'}):
            self.assertFalse(target.eh_posicao(case))

    def test_posicao_para_str(self):
        """
        Testa posicao_para_str para todas as posições válidas possíveis
        """
        for case in self.positions:
            pos = target.cria_posicao(case[0], case[1])
            self.assertEqual(target.posicao_para_str(pos), case[0] + case[1])

    def test_obter_posicoes_adjacentes(self):
        """
        Testa obter_posicoes_adjacentes para todas as posições válidas possíveis
        """

        result = (
            (('b', '1'), ('a', '2'), ('b', '2')),
            (('a', '1'), ('b', '2'), ('a', '3')),
            (('a', '2'), ('b', '2'), ('b', '3')),
            (('a', '1'), ('c', '1'), ('b', '2')),
            (('a', '1'), ('b', '1'), ('c', '1'), ('a', '2'),
             ('c', '2'), ('a', '3'), ('b', '3'), ('c', '3')),
            (('b', '2'), ('a', '3'), ('c', '3')),
            (('b', '1'), ('b', '2'), ('c', '2')),
            (('c', '1'), ('b', '2'), ('c', '3')),
            (('b', '2'), ('c', '2'), ('b', '3'))
        )

        for i in range(len(self.positions)):
            c, l = self.positions[i]
            pos = target.cria_posicao(c, l)
            correctResult = tuple(target.cria_posicao(
                x[0], x[1]) for x in result[i])
            self.assertEqual(
                correctResult, target.obter_posicoes_adjacentes(pos))

    _cria_posicao, _cria_copia_posicao, _obter_pos_c, _obter_pos_l, \
        _eh_posicao, _posicoes_iguais, _posicao_para_str = (
        lambda c, l: {n: 'c' if chr(n) == c else 'l' if chr(n) == l \
                      else '' for n in range(122,-1,-1)},
        lambda p: {k:v for (k,v) in p.item()},
        lambda p: chr([k for (k,v) in p.items() if v == 'c'][0]),
        lambda p: chr([k for (k,v) in p.items() if v == 'l'][0]),
        lambda p: type(p) == dict and [*p.keys()] == [*range(122,-1,-1)] and \
            [*p.values()].count('c') == [*p.values()].count('l') == 1,
        lambda p1, p2: type(p1) == type(p2) == dict and \
            [*p1.keys()] == [*p2.keys()] == [*range(122,-1,-1)] and \
            [*p1.values(),*p2.values()].count('c') == \
            [*p1.values(),*p2.values()].count('l') == 2 and \
            eh_posicao(p1) and eh_posicao(p2) and \
            [*p1.values()].index('c') == [*p2.values()].index('c') and \
            [*p1.values()].index('l') == [*p2.values()].index('l'),
        lambda p: ''.join([chr(k) for (k,v) in p.items() if v in ('c', 'l')][::-1])
    )

    @patch.object(target, 'cria_posicao', side_effect = _cria_posicao)
    @patch.object(target, 'cria_copia_posicao', side_effect = _cria_copia_posicao)
    @patch.object(target, 'obter_pos_c', side_effect = _obter_pos_c)
    @patch.object(target, 'obter_pos_l', side_effect = _obter_pos_l)
    @patch.object(target, 'eh_posicao', side_effect = _eh_posicao)
    @patch.object(target, 'posicoes_iguais', side_effect = _posicoes_iguais)
    @patch.object(target, 'posicao_para_str', side_effect = _posicao_para_str)
    def test_posicao_abstracao(self, *_):
        """
        Testa as barreiras de abstração do TAD Posição
        """

        # NOTE: Esta implementação de TAD foi criada de propósito para ser absurda,
        #   copiar isto seria extremamente obvio e uma má decisão académica

        self.test_obter_posicoes_adjacentes()



class TestTADPeca(unittest.TestCase):
    def setUp(self):
        self.pieces = list('XO ')
        self.invalid_pieces = (True, False, 4, 1.45, 'x', 'o', '\t', '\u200B', {
                               'foo': 'bar'}, ['foo', 'bar'], ('foo', 'bar'))

    def test_cria_peca_fail(self):
        """
        Testa a verificação dos argumentos no cria_peca.
        Todos os casos devem retornar ValueError.
        """
        for piece in self.invalid_pieces + (0, -1, 1):
            with self.assertRaises(ValueError, msg='ValueError not raised for {}'.format(piece)) as ctx:
                target.cria_peca(piece)
            self.assertEqual(
                'cria_peca: argumento invalido', str(ctx.exception))

    def test_cria_peca_success(self):
        """
        Testa a criação das pecas sem retornar ValueError.
        Todas as 3 pecas possiveis são testadas.
        """
        for piece in self.pieces:
            try:
                target.cria_peca(piece)
            except ValueError:
                self.fail("cria_peca raised ValueError when it shouldn't")

    def test_cria_copia_peca(self):
        """
        Testa a criação de uma cópia de todas as pecas possíveis.
        Relembra-se que a cópia não pode ser o mesmo objeto que o original,
        isto é, "original is copia" tem de retornar False.
        """
        for piece in self.pieces:
            original = target.cria_peca(piece)
            copy = target.cria_copia_peca(original)
            self.assertIsNot(original, copy)
            self.assertTrue(target.pecas_iguais(original, copy))

    def test_pecas_iguais_success(self):
        """
        Testa pecas_iguais para todas as peças válidas possíveis
        """
        for pieces in self.pieces:
            p1 = target.cria_peca(pieces)
            p2 = target.cria_peca(pieces)
            self.assertTrue(target.pecas_iguais(p1, p2))

    def test_pecas_iguais_fail(self):
        """
        Testa pecas_iguais para peças diferentes
        """
        p1 = target.cria_peca('X')
        p2 = target.cria_peca('O')
        self.assertFalse(target.pecas_iguais(p1, p2))

        for piece in self.invalid_pieces:
            # invalid pieces should return false
            self.assertFalse(target.pecas_iguais(piece, piece))

    def test_eh_peca_success(self):
        """
        Testa eh_peca para todas as peças válidas possíveis
        """
        for piece in self.pieces:
            p1 = target.cria_peca(piece)
            self.assertTrue(target.eh_peca(p1))

    def test_eh_peca_fail(self):
        """
        Testa eh_peca para objetos que não sejam peças
        """
        for piece in self.invalid_pieces:
            self.assertFalse(target.eh_peca(piece))

    def test_peca_para_str(self):
        """
        Testa peca_para_str para todas as peºas válidas possíveis
        """
        for piece in self.pieces:
            p = target.cria_peca(piece)
            self.assertEqual(target.peca_para_str(p), '[' + piece + ']')

    def test_peca_para_inteiro(self):
        """
        Testa peca_para_inteiro para todas as peças válidas possíveis
        """

        result = (1, -1, 0)

        for i in range(len(self.pieces)):
            piece = self.pieces[i]
            p = target.cria_peca(piece)
            self.assertEqual(result[i], target.peca_para_inteiro(p))

    _cria_peca, _cria_copia_peca, _eh_peca, _pecas_iguais, _peca_para_str = (
        lambda s: {'foo' : 'bar'.join([chr(n) for n in range(ord(s))])},
        lambda j: {'foo': j['foo']},
        lambda j: j in tuple({'foo' : 'bar'.join([chr(n) for n in range(m)])}\
                             for m in (32,88,79)),
        lambda j1, j2: all(j in tuple({'foo' : 'bar'.join(
            [chr(n) for n in range(m)])} for m in (32,88,79))\
                           for j in (j1, j2)) and len(j1['foo']) == len(j2['foo']),
        lambda j: ''.join(
            [chr(n) if n != 92 else chr(ord(j['foo'][-1]) + 1) for n in range(91, 94)])
    )

    @patch.object(target, 'cria_peca', side_effect = _cria_peca)
    @patch.object(target, 'cria_copia_peca', side_effect = _cria_copia_peca)
    @patch.object(target, 'eh_peca', side_effect = _eh_peca)
    @patch.object(target, 'pecas_iguais', side_effect = _pecas_iguais)
    @patch.object(target, 'peca_para_str', side_effect = _peca_para_str)
    def test_peca_abstracao(self, *_):
        """
        Testa as barreiras de abstração do TAD Peca
        """

        # NOTE: Esta implementação de TAD foi criada de propósito para ser absurda,
        #   copiar isto seria extremamente obvio e uma má decisão académica

        self.test_peca_para_inteiro()


class TestTADTabuleiro(unittest.TestCase):

    def setUp(self):
        self.valid_boards = [
            ((0, 0, 0), (0, 0, 0), (0, 0, 0)),
            ((0, -1, 0), (1, 0, 0), (0, 1, 0)),
            ((1, 0, -1), (1, -1, 0), (1, 0, 0))
        ]

        self.invalid_boards = [
            ((0, 1, 0), (1, 0, 0), (0, 0, 0)),
            ((-1, 0, 0), (1, 0, 0), (-1, 0, -1)),
            ((1, 0, -1), (0, -1, 1), (1, 1, -1)),
            ((1, 0, -1), (1, 0, -1), (1, 0, -1)),
            ((1, 1, 1), (0, 0, 0), (-1, -1, -1))
        ]

        self.not_boards = [True, False, 1, 0.5, 3.454, 'foobar']

        self.position_map = (
            ('a', '1', 0, 0),
            ('b', '1', 0, 1),
            ('c', '1', 0, 2),
            ('a', '2', 1, 0),
            ('b', '2', 1, 1),
            ('c', '2', 1, 2),
            ('a', '3', 2, 0),
            ('b', '3', 2, 1),
            ('c', '3', 2, 2)
        )

    def test_cria_tabuleiro(self):
        """
        Testa que a função cria_tabuleiro não dá erros.
        """
        try:
            target.cria_tabuleiro()
        except:
            self.fail("Function cria_tabuleiro raises error when it shouldn't")

    def test_cria_copia_tabuleiro(self):
        """
        Testa a criação de uma cópia de vários tabuleiros válidos.
        Relembra-se que a cópia não pode ser o mesmo objeto que o original,
        isto é, "original is copia" tem de retornar False.
        """
        for board in self.valid_boards:
            original = target.tuplo_para_tabuleiro(board)
            copy = target.cria_copia_tabuleiro(original)
            self.assertIsNot(original, copy)
            self.assertTrue(target.tabuleiros_iguais(original, copy))

    def test_obter_peca(self):
        """
        Testa para tabuleiros válidos, que o valor de retorno da função
        obter_peca retorna a peça na posição dada.
        """
        for board in self.valid_boards:
            board_obj = target.tuplo_para_tabuleiro(board)
            for pos in self.position_map:
                correct_result = board[pos[2]][pos[3]]
                result = target.obter_peca(
                    board_obj, target.cria_posicao(pos[0], pos[1]))
                self.assertEqual(
                    correct_result, target.peca_para_inteiro(result))

    def test_eh_tabuleiro_success(self):
        """
        Testa eh_tabuleiro para tabuleiros válidos (que retornem True).
        """
        for board in self.valid_boards:
            board_obj = target.tuplo_para_tabuleiro(board)
            self.assertTrue(target.eh_tabuleiro(board_obj))

    def test_eh_tabuleiro_fail(self):
        """
        Testa eh_tabuleiro para tabuleiros inválidos (que retornem False).
        """
        for board in self.invalid_boards:
            board_obj = target.tuplo_para_tabuleiro(board)
            self.assertFalse(target.eh_tabuleiro(board_obj))

        for board in self.not_boards:
            self.assertFalse(target.eh_tabuleiro(board))

    def test_tabuleiros_iguais_success(self):
        """
        Testa tabuleiros_iguais para tabuleiros iguais
        """
        for board in self.valid_boards:
            b1 = target.tuplo_para_tabuleiro(board)
            b2 = target.tuplo_para_tabuleiro(board)
            self.assertTrue(target.tabuleiros_iguais(b1, b2))

    def test_tabuleiros_iguais_fail(self):
        """
        Testa tabuleiros_iguais para tabuleiros diferentes
        """
        b1 = self.valid_boards[0]
        for board in self.valid_boards[1:]:
            b2 = target.tuplo_para_tabuleiro(board)
            self.assertFalse(target.tabuleiros_iguais(b1, b2))

        for board in self.invalid_boards:
            # invalid boards should return false
            self.assertFalse(target.tabuleiros_iguais(board, board))


class TestTabuleiroParaStr(unittest.TestCase):
    def test_tabuleiro_para_str(self):
        """
        Str do tabuleiro vazio
        """
        data = target.cria_tabuleiro()

        result = target.tabuleiro_para_str(data)

        self.assertEqual(
            result,
            "   a   b   c\n1 [ ]-[ ]-[ ]\n   | \\ | / |\n2 [ ]-[ ]-[ ]\n   | / | \\ |\n3 [ ]-[ ]-[ ]",
        )


class TestPecasIguais(unittest.TestCase):
    def test_pecas_iguais(self):
        result = target.pecas_iguais(
            target.cria_peca("X"), target.cria_peca("O"))

        self.assertEqual(result, False)


class TestPecaParaStr(unittest.TestCase):
    def test_peca_para_str(self):
        result = target.peca_para_str(target.cria_peca("X"))
        self.assertEqual(result, "[X]")


class TestPecaParaInteiro(unittest.TestCase):
    def test_peca_para_inteiro(self):
        result = target.peca_para_inteiro(target.cria_peca(" "))

        self.assertEqual(result, 0)


class TestColocaPeca(unittest.TestCase):
    def test_coloca_peca(self):
        data1 = target.cria_tabuleiro()
        data2 = target.cria_peca("X")
        data3 = target.cria_posicao("a", "1")

        result = target.tabuleiro_para_str(
            target.coloca_peca(data1, data2, data3))

        self.assertEqual(
            result,
            "   a   b   c\n1 [X]-[ ]-[ ]\n   | \\ | / |\n2 [ ]-[ ]-[ ]\n   | / | \\ |\n3 [ ]-[ ]-[ ]",
        )


class TestMovePeca(unittest.TestCase):
    def test_move_peca(self):
        data1 = target.cria_tabuleiro()
        data2 = target.cria_peca("X")
        data3 = target.cria_posicao("a", "1")
        data4 = target.coloca_peca(data1, data2, data3)
        data5 = target.cria_posicao("b", "1")

        result = target.tabuleiro_para_str(
            target.move_peca(data4, data3, data5))

        self.assertEqual(
            result,
            "   a   b   c\n1 [ ]-[X]-[ ]\n   | \\ | / |\n2 [ ]-[ ]-[ ]\n   | / | \\ |\n3 [ ]-[ ]-[ ]",
        )


class TestObterGanhador(unittest.TestCase):
    def test_obter_ganhador(self):
        data = target.tuplo_para_tabuleiro(
            ((0, 1, -1), (-0, 1, -1), (1, 0, -1)))

        result = target.peca_para_str(target.obter_ganhador(data))

        self.assertEqual(result, "[O]")


class TestObterPosicoesLivres(unittest.TestCase):
    def test_obter_posicoes_livres(self):
        data = target.tuplo_para_tabuleiro(
            ((0, 1, -1), (-0, 1, -1), (1, 0, -1)))

        result = tuple(
            target.posicao_para_str(p) for p in target.obter_posicoes_livres(data)
        )

        self.assertEqual(result, ("a1", "a2", "b3"))


class TestObterVetor(unittest.TestCase):
    def test_obter_vetor_1(self):
        data = target.tuplo_para_tabuleiro(
            ((0, 1, -1), (-0, 1, -1), (1, 0, -1)))

        result = tuple(
            target.peca_para_str(peca) for peca in target.obter_vetor(data, "a")
        )

        self.assertEqual(result, ("[ ]", "[ ]", "[X]"))

    def test_obter_vetor_2(self):
        data = target.tuplo_para_tabuleiro(
            ((0, 1, -1), (-0, 1, -1), (1, 0, -1)))

        result = tuple(
            target.peca_para_str(peca) for peca in target.obter_vetor(data, "2")
        )

        self.assertEqual(result, ("[ ]", "[X]", "[O]"))


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])
