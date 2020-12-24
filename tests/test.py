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
                'cria_posicao: argumentos invalidos', str(ctx.exception),
                msg='Falhou nos inputs {}, {}'.format(case[0], case[1]))

    def test_cria_posicao_success(self):
        """
        Testa a criação dos argumentos sem retornar ValueError.
        Todas as 9 posições possiveis são testadas.
        """
        for case in self.positions:
            try:
                target.cria_posicao(case[0], case[1])
            except ValueError:
                self.fail("cria_posicao raised ValueError when it shouldn't. Input: {}, {}".format(
                    case[0], case[1]))

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
                correctResult, target.obter_posicoes_adjacentes(pos), 'Falhou na posicao ' + c + l)

    mocks = (
        lambda c, l: {n: 'c' if chr(n) == c else 'l' if chr(n) == l
                      else '' for n in range(122, -1, -1)},
        lambda p: {k: v for (k, v) in p.item()},
        lambda p: chr([k for (k, v) in p.items() if v == 'c'][0]),
        lambda p: chr([k for (k, v) in p.items() if v == 'l'][0]),
        lambda p: type(p) == dict and [*p.keys()] == [*range(123)] and
        [*p.values()].count('c') == [*p.values()].count('l') == 1,
        lambda p1, p2: type(p1) == type(p2) == dict and
        [*p1.keys()] == [*p2.keys()] == [*range(123)] and
        [*p1.values(), *p2.values()].count('c') ==
        [*p1.values(), *p2.values()].count('l') == 2 and
        [*p1.values()].index('c') == [*p2.values()].index('c') and
        [*p1.values()].index('l') == [*p2.values()].index('l'),
        lambda p: ''.join([chr(k)
                           for (k, v) in p.items() if v in ('c', 'l')][::-1])
    )

    @patch.object(target, 'cria_posicao', side_effect=mocks[0])
    @patch.object(target, 'cria_copia_posicao', side_effect=mocks[1])
    @patch.object(target, 'obter_pos_c', side_effect=mocks[2])
    @patch.object(target, 'obter_pos_l', side_effect=mocks[3])
    @patch.object(target, 'eh_posicao', side_effect=mocks[4])
    @patch.object(target, 'posicoes_iguais', side_effect=mocks[5])
    @patch.object(target, 'posicao_para_str', side_effect=mocks[6])
    def test_obter_posicoes_adjacentes_mock(self, *_):
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

    mocks = (
        lambda s: {'foo': 'bar'.join([chr(n) for n in range(ord(s))])},
        lambda j: {'foo': j['foo']},
        lambda j: j in tuple({'foo': 'bar'.join([chr(n) for n in range(m)])}
                             for m in (32, 88, 79)),
        lambda j1, j2: all(j in tuple({'foo': 'bar'.join(
            [chr(n) for n in range(m)])} for m in (32, 88, 79))
            for j in (j1, j2)) and len(j1['foo']) == len(j2['foo']),
        lambda j: ''.join(
            [chr(n) if n != 92 else chr(ord(j['foo'][-1]) + 1) for n in range(91, 94)])
    )

    @patch.object(target, 'cria_peca', side_effect=mocks[0])
    @patch.object(target, 'cria_copia_peca', side_effect=mocks[1])
    @patch.object(target, 'eh_peca', side_effect=mocks[2])
    @patch.object(target, 'pecas_iguais', side_effect=mocks[3])
    @patch.object(target, 'peca_para_str', side_effect=mocks[4])
    def test_peca_para_inteiro_mock(self, *_):
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
            ((1, 0, -1), (1, -1, 0), (1, 0, 0)),
            ((1, -1, 0), (-1, 0, 1), (0, -1, 1)),
            ((1, 0, -1), (-1, 0, 1), (0, 0, 1))
        ]

        self.valid_boards_vertical_vectors = [
            ((0, 0, 0), (0, 0, 0), (0, 0, 0)),
            ((0, 1, 0), (-1, 0, 1), (0, 0, 0)),
            ((1, 1, 1), (0, -1, 0), (-1, 0, 0)),
            ((1, -1, 0), (-1, 0, -1), (0, 1, 1)),
            ((1, -1, 0), (0, 0, 0), (-1, 1, 1))
        ]

        self.valid_boards_winners = [0, 0, 1, 0, 0]
        self.valid_boards_free = [
            ('a1', 'b1', 'c1', 'a2', 'b2', 'c2', 'a3', 'b3', 'c3'),
            ('a1', 'c1', 'b2', 'c2', 'a3', 'c3'),
            ('b1', 'c2', 'b3', 'c3'),
            ('c1', 'b2', 'a3'),
            ('b1', 'b2', 'a3', 'b3')
        ]
        self.valid_boards_piece = [
            {
                'X': (),
                'O': (),
            },
            {
                'X': ('a2', 'b3'),
                'O': ('b1', ),
            },
            {
                'X': ('a1', 'a2', 'a3'),
                'O': ('c1', 'b2'),
            },
            {
                'X': ('a1', 'c2', 'c3'),
                'O': ('b1', 'a2', 'b3'),
            },
            {
                'X': ('a1', 'c2', 'c3'),
                'O': ('c1', 'a2')
            }
        ]

        self.valid_boards_str = [
            "   a   b   c\n1 [ ]-[ ]-[ ]\n   | \\ | / |\n2 [ ]-[ ]-[ ]\n   | / | \\ |\n3 [ ]-[ ]-[ ]",
            "   a   b   c\n1 [ ]-[O]-[ ]\n   | \\ | / |\n2 [X]-[ ]-[ ]\n   | / | \\ |\n3 [ ]-[X]-[ ]",
            "   a   b   c\n1 [X]-[ ]-[O]\n   | \\ | / |\n2 [X]-[O]-[ ]\n   | / | \\ |\n3 [X]-[ ]-[ ]",
            "   a   b   c\n1 [X]-[O]-[ ]\n   | \\ | / |\n2 [O]-[ ]-[X]\n   | / | \\ |\n3 [ ]-[O]-[X]",
            "   a   b   c\n1 [X]-[ ]-[O]\n   | \\ | / |\n2 [O]-[ ]-[X]\n   | / | \\ |\n3 [ ]-[ ]-[X]"
        ]

        self.invalid_boards = [
            ((0, 1, 0), (1, 0, 0), (0, 0, 0)),
            ((-1, 0, 0), (1, 0, 0), (-1, 0, -1)),
            ((1, 0, -1), (0, -1, 1), (1, 1, -1)),
            ((1, 0, -1), (1, 0, -1), (1, 0, -1)),
            ((1, 1, 1), (0, 0, 0), (-1, -1, -1)),
            ((1, 0, 0), (-1, -1, 0), (-1, 0, 0)),
            ((1, 1, -1), (1, 0, -1), (-1, 1, 0))
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

        self.vectors = ['a', 'b', 'c', '1', '2', '3']

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
            self.assertTrue(target.eh_tabuleiro(board_obj),
                            msg="Input: {}".format(board))

    def test_eh_tabuleiro_fail(self):
        """
        Testa eh_tabuleiro para tabuleiros inválidos (que retornem False).
        """
        for board in self.invalid_boards:
            board_obj = target.tuplo_para_tabuleiro(board)
            self.assertFalse(target.eh_tabuleiro(board_obj),
                             msg="Input: {}".format(board))

        for board in self.not_boards:
            self.assertFalse(target.eh_tabuleiro(board),
                             msg="Input: {}".format(board))

    def test_tabuleiros_iguais_success(self):
        """
        Testa tabuleiros_iguais para tabuleiros iguais
        """
        for board in self.valid_boards:
            b1 = target.tuplo_para_tabuleiro(board)
            b2 = target.tuplo_para_tabuleiro(board)
            self.assertTrue(target.tabuleiros_iguais(
                b1, b2), msg="Input: {}".format(board))

    def test_tabuleiros_iguais_fail(self):
        """
        Testa tabuleiros_iguais para tabuleiros diferentes
        """
        b1 = self.valid_boards[0]
        for board in self.valid_boards[1:]:
            board1 = target.tuplo_para_tabuleiro(b1)
            b2 = target.tuplo_para_tabuleiro(board)
            self.assertFalse(target.tabuleiros_iguais(
                board1, b2), msg="Input: {}, {}".format(b1, board))

        for board in self.invalid_boards:
            # invalid boards should return false
            board_obj = target.tuplo_para_tabuleiro(board)
            self.assertFalse(target.tabuleiros_iguais(
                board_obj, board_obj), msg="Input: {}".format(board))

    def test_obter_vetor(self):
        """
        Testa obter_vetor para todos os vetores em tabuleiros válidos
        """
        for j in range(len(self.valid_boards)):
            board = self.valid_boards[j]
            board_obj = target.tuplo_para_tabuleiro(board)
            for i in range(len(self.vectors)):
                vector = self.vectors[i]
                result = tuple(target.peca_para_inteiro(x)
                               for x in target.obter_vetor(board_obj, vector))
                correct_result = self.valid_boards_vertical_vectors[j][i] if i < 3 else board[i - 3]
                self.assertEqual(result, correct_result,
                                 msg="Input: {}, {}".format(board, vector))

    def test_tabuleiro_para_str(self):
        """
        Testa a conversão do tabuleiro para a sua representação em string
        """
        for i in range(len(self.valid_boards)):
            board = self.valid_boards[i]
            self.assertEqual(self.valid_boards_str[i], target.tabuleiro_para_str(
                target.tuplo_para_tabuleiro(board)), msg="Input: {}".format(board))

    def test_eh_posicao_livre(self):
        """
        Testa eh_posicao_livre para todas as posições de tabuleiros válidos
        """
        for board in self.valid_boards:
            board_obj = target.tuplo_para_tabuleiro(board)
            for pos in self.position_map:
                pos_obj = target.cria_posicao(pos[0], pos[1])
                self.assertEqual(target.eh_posicao_livre(
                    board_obj, pos_obj), board[pos[2]][pos[3]] == 0, msg="Input: {}, {}".format(board, pos[0] + pos[1]))

    def test_coloca_peca(self):
        """
        Testa coloca_peca para uma posicao num tabuleiro
        """
        board = target.cria_tabuleiro()
        empty_piece = target.cria_peca(' ')
        piece = target.cria_peca('X')
        target_pos = target.cria_posicao('a', '1')

        self.assertEqual(target.obter_peca(board, target_pos), empty_piece)
        new_board = target.coloca_peca(board, piece, target_pos)
        # coloca_peca should return the same board
        self.assertIs(board, new_board)
        self.assertTrue(target.pecas_iguais(
            piece, target.obter_peca(board, target_pos)))

    def test_move_peca(self):
        """
        Testa move_peca de uma posicao para outra num tabuleiro
        """
        board = target.tuplo_para_tabuleiro(self.valid_boards[3])
        pos_from = target.cria_posicao('b', '3')
        pos_to = target.cria_posicao('a', '3')

        piece = target.cria_peca('O')

        new_board = target.move_peca(board, pos_from, pos_to)
        # move_peca should return the same board
        self.assertIs(board, new_board)
        self.assertTrue(target.pecas_iguais(
            piece, target.obter_peca(new_board, pos_to)))

    def test_remove_peca(self):
        """
        Testa remove_peca numa posicao de um tabuleiro
        """
        board = target.tuplo_para_tabuleiro(self.valid_boards[2])
        pos = target.cria_posicao('a', '2')

        piece = target.cria_peca('X')
        empty_piece = target.cria_peca(' ')

        self.assertTrue(target.pecas_iguais(
            piece, target.obter_peca(board, pos)))
        new_board = target.remove_peca(board, pos)
        # remove_peca should return the same board
        self.assertIs(board, new_board)
        self.assertTrue(target.pecas_iguais(
            empty_piece, target.obter_peca(board, pos)))

    def test_obter_ganhador(self):
        """
        Testa obter_ganhador para vários tabuleiros válidos
        """
        for i in range(len(self.valid_boards)):
            board = target.tuplo_para_tabuleiro(self.valid_boards[i])
            winner = self.valid_boards_winners[i]

            winner_result = target.obter_ganhador(board)
            self.assertEqual(winner, target.peca_para_inteiro(
                winner_result), msg="Input: {}".format(board))

    def test_obter_posicoes_livres(self):
        """
        Testa obter_posicoes_livres para varios tabuleiros válidos
        """
        for i in range(len(self.valid_boards)):
            board = target.tuplo_para_tabuleiro(self.valid_boards[i])
            empty_positions = self.valid_boards_free[i]

            empty_positions_result = target.obter_posicoes_livres(board)

            self.assertEqual(type(empty_positions_result), tuple)
            self.assertEqual(tuple(target.posicao_para_str(x)
                                   for x in empty_positions_result), empty_positions, msg="Input: {}".format(board))

    def test_obter_posicoes_jogador(self):
        """
        Testa obter_posicoes_livres para varios tabuleiros válidos
        """
        for i in range(len(self.valid_boards)):
            board = target.tuplo_para_tabuleiro(self.valid_boards[i])
            for player in self.valid_boards_piece[i]:
                pos = self.valid_boards_piece[i][player]

                piece = target.cria_peca(player)
                pos_result = target.obter_posicoes_jogador(board, piece)

                self.assertEqual(type(pos_result), tuple)
                self.assertEqual(tuple(target.posicao_para_str(x)
                                       for x in pos_result), pos, msg="Input: {}, {}".format(board, player))

    mocks = TestTADPosicao.mocks

    @patch.object(target, 'cria_posicao', side_effect=mocks[0])
    @patch.object(target, 'cria_copia_posicao', side_effect=mocks[1])
    @patch.object(target, 'obter_pos_c', side_effect=mocks[2])
    @patch.object(target, 'obter_pos_l', side_effect=mocks[3])
    @patch.object(target, 'eh_posicao', side_effect=mocks[4])
    @patch.object(target, 'posicoes_iguais', side_effect=mocks[5])
    @patch.object(target, 'posicao_para_str', side_effect=mocks[6])
    def test_abstracao_posicao_no_tabuleiro(self, *_):
        """
        Testa as barreiras de abstração do TAD tabuleiro em relação ao TAD posição
        """
        self.test_cria_tabuleiro()
        self.test_cria_copia_tabuleiro()
        self.test_obter_peca()
        self.test_eh_tabuleiro_success()
        self.test_eh_tabuleiro_fail()
        self.test_tabuleiros_iguais_success()
        self.test_tabuleiros_iguais_fail()
        self.test_obter_vetor()
        self.test_tabuleiro_para_str()
        self.test_eh_posicao_livre()
        self.test_coloca_peca()
        self.test_move_peca()
        self.test_remove_peca()
        self.test_obter_ganhador()
        self.test_obter_posicoes_livres()
        self.test_obter_posicoes_jogador()

    mocks = TestTADPeca.mocks

    @patch.object(target, 'cria_peca', side_effect=mocks[0])
    @patch.object(target, 'cria_copia_peca', side_effect=mocks[1])
    @patch.object(target, 'eh_peca', side_effect=mocks[2])
    @patch.object(target, 'pecas_iguais', side_effect=mocks[3])
    @patch.object(target, 'peca_para_str', side_effect=mocks[4])
    def test_abstracao_peca_no_tabuleiro(self, *_):
        """
        Testa as barreiras de abstração do TAD tabuleiro em relação ao TAD peca
        """
        self.test_cria_tabuleiro()
        self.test_cria_copia_tabuleiro()
        self.test_obter_peca()
        self.test_eh_tabuleiro_success()
        self.test_eh_tabuleiro_fail()
        self.test_tabuleiros_iguais_success()
        self.test_tabuleiros_iguais_fail()
        self.test_obter_vetor()
        self.test_tabuleiro_para_str()
        self.test_eh_posicao_livre()
        self.test_coloca_peca()
        self.test_move_peca()
        self.test_remove_peca()
        self.test_obter_ganhador()
        self.test_obter_posicoes_livres()
        self.test_obter_posicoes_jogador()


class TestFuncoesAdicionais(unittest.TestCase):

    def setUp(self):
        self.easyAuto = [
            (((-1, 0, 0), (1, 1, 0), (0, 0, 0)), 'O', ('c2', )),
            (((1, 1, 0), (1, -1, 0), (-1, 0, 0)), 'O', ('c1', )),
            (((1, 1, 0), (-1, -1, 0), (0, 0, 0)), 'X', ('c1', )),
            (((1, 1, 0), (-1, -1, 0), (0, 0, 0)), 'O', ('c2', )),
            (((-1, 0, 1), (1, -1, 0), (0, 0, 0)), 'X', ('a3', )),
            (((-1, 0, 1), (1, -1, 0), (0, 0, 0)), 'O', ('a3', )),
            (((0, -1, -1), (-1, 1, 0), (1, 0, 1)), 'X', ('b2', 'a1')),
            (((0, -1, 0), (-1, 1, 1), (-1, 0, 1)), 'X', ('b2', 'a1')),
            (((0, 1, 0), (-1, 1, 0), (-1, -1, 1)), 'X', ('b1', 'a1')),
            (((-1, 1, 0), (0, -1, 1), (-1, 0, 1)), 'O', ('a1', 'a2')),
            (((-1, 1, 0), (0, -1, 1), (-1, 0, 1)), 'X', ('b1', 'c1'))
        ]

        self.normalAuto = [
            (((-1, 0, 0), (1, 1, 0), (0, 0, 0)), 'O', ('c2', )),
            (((1, 1, 0), (1, -1, 0), (-1, 0, 0)), 'O', ('c1', )),
            (((1, 1, 0), (-1, -1, 0), (0, 0, 0)), 'X', ('c1', )),
            (((1, 1, 0), (-1, -1, 0), (0, 0, 0)), 'O', ('c2', )),
            (((-1, 0, 1), (1, -1, 0), (0, 0, 0)), 'X', ('a3', )),
            (((-1, 0, 1), (1, -1, 0), (0, 0, 0)), 'O', ('a3', )),
            (((0, -1, -1), (-1, 1, 0), (1, 0, 1)), 'X', ('b2', 'b3')),
            (((0, -1, 0), (-1, 1, 1), (-1, 0, 1)), 'X', ('b2', 'c1')),
            (((0, 1, -1), (0, 1, -1), (1, -1, 0)), 'X', ('b1', 'a1')),
            (((-1, 1, 1), (1, -1, 0), (0, 0, -1)), 'O', ('b2', 'c2')),
            (((-1, 1, 0), (0, 1, 0), (-1, -1, 1)), 'O', ('a1', 'a2')),
            (((0, 1, 0), (-1, 1, 0), (-1, -1, 1)), 'X', ('b1', 'a1')),
            (((0, 1, -1), (0, -1, 1), (-1, 0, 1)), 'O', ('b2', 'a1')),
            (((-1, 1, 0), (0, -1, 1), (-1, 0, 1)), 'O', ('b2', 'a2')),
            (((-1, 1, 0), (0, -1, 1), (-1, 0, 1)), 'X', ('b1', 'c1'))
        ]

        self.hardAuto = [
            (((-1, 0, 0), (1, 1, 0), (0, 0, 0)), 'O', ('c2', )),
            (((1, 1, 0), (1, -1, 0), (-1, 0, 0)), 'O', ('c1', )),
            (((1, 1, 0), (-1, -1, 0), (0, 0, 0)), 'X', ('c1', )),
            (((1, 1, 0), (-1, -1, 0), (0, 0, 0)), 'O', ('c2', )),
            (((-1, 0, 1), (1, -1, 0), (0, 0, 0)), 'X', ('a3', )),
            (((-1, 0, 1), (1, -1, 0), (0, 0, 0)), 'O', ('a3', )),
            (((0, 1, -1), (0, 1, -1), (1, -1, 0)), 'X', ('b2', 'c3')),
            (((-1, 1, 1), (1, -1, 0), (0, 0, -1)), 'O', ('c3', 'c2')),
            (((-1, 1, 0), (0, 1, 0), (-1, -1, 1)), 'O', ('a3', 'a2')),
            (((0, 1, 0), (-1, 1, 0), (-1, -1, 1)), 'O', ('a2', 'a1')),
            (((0, 1, 0), (-1, 1, 0), (-1, -1, 1)), 'X', ('b1', 'c1')),
            (((0, 1, -1), (0, -1, 1), (-1, 0, 1)), 'O', ('a3', 'b3')),
            (((-1, 1, 0), (0, -1, 1), (-1, 0, 1)), 'O', ('b2', 'a2')),
            (((-1, 1, 0), (0, -1, 1), (-1, 0, 1)), 'X', ('b1', 'c1'))
        ]

    def test_obter_movimento_auto_facil(self):
        """
        Testa obter_movimento_auto com a dificuldade 'facil'
        """

        for board, player, correct_result in self.easyAuto:
            board_obj = target.tuplo_para_tabuleiro(board)
            player_obj = target.cria_peca(player)
            result = target.obter_movimento_auto(
                board_obj, player_obj, 'facil')
            self.assertEqual(type(result), tuple)
            result_formatted = tuple(target.posicao_para_str(x)
                                     for x in result)
            self.assertEqual(correct_result, result_formatted,
                             msg="Input: {}, {}".format(board, player))

    def test_obter_movimento_auto_normal(self):
        """
        Testa obter_movimento_auto com a dificuldade 'normal'
        """

        for board, player, correct_result in self.normalAuto:
            board_obj = target.tuplo_para_tabuleiro(board)
            player_obj = target.cria_peca(player)
            result = target.obter_movimento_auto(
                board_obj, player_obj, 'normal')
            self.assertEqual(type(result), tuple)
            result_formatted = tuple(target.posicao_para_str(x)
                                     for x in result)
            self.assertEqual(correct_result, result_formatted,
                             msg="Input: {}, {}".format(board, player))

    def test_obter_movimento_auto_dificil(self):
        """
        Testa obter_movimento_auto com a dificuldade 'dificil'
        """

        for board, player, correct_result in self.hardAuto:
            board_obj = target.tuplo_para_tabuleiro(board)
            player_obj = target.cria_peca(player)
            result = target.obter_movimento_auto(
                board_obj, player_obj, 'dificil')
            self.assertEqual(type(result), tuple)
            result_formatted = tuple(target.posicao_para_str(x)
                                     for x in result)
            self.assertEqual(correct_result, result_formatted,
                             msg="Input: {}, {}".format(board, player))

    mocks = TestTADPosicao.mocks

    @patch.object(target, 'cria_posicao', side_effect=mocks[0])
    @patch.object(target, 'cria_copia_posicao', side_effect=mocks[1])
    @patch.object(target, 'obter_pos_c', side_effect=mocks[2])
    @patch.object(target, 'obter_pos_l', side_effect=mocks[3])
    @patch.object(target, 'eh_posicao', side_effect=mocks[4])
    @patch.object(target, 'posicoes_iguais', side_effect=mocks[5])
    @patch.object(target, 'posicao_para_str', side_effect=mocks[6])
    def test_abstracao_posicao_nas_adicionais(self, *_):
        """
        Testa as barreiras de abstração das funções adicionais em relação ao TAD posição
        """
        self.test_obter_movimento_auto_facil()
        self.test_obter_movimento_auto_normal()
        self.test_obter_movimento_auto_dificil()


    mocks = TestTADPeca.mocks

    @patch.object(target, 'cria_peca', side_effect=mocks[0])
    @patch.object(target, 'cria_copia_peca', side_effect=mocks[1])
    @patch.object(target, 'eh_peca', side_effect=mocks[2])
    @patch.object(target, 'pecas_iguais', side_effect=mocks[3])
    @patch.object(target, 'peca_para_str', side_effect=mocks[4])
    def test_abstracao_peca_nas_adicionais(self, *_):
        """
        Testa as barreiras de abstração das funções adicionais em relação ao TAD peca
        """
        self.test_obter_movimento_auto_facil()
        self.test_obter_movimento_auto_normal()
        self.test_obter_movimento_auto_dificil()


class TestsEnunciado(unittest.TestCase):
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

    def test_pecas_iguais(self):
        result = target.pecas_iguais(
            target.cria_peca("X"), target.cria_peca("O"))

        self.assertEqual(result, False)

    def test_peca_para_str(self):
        result = target.peca_para_str(target.cria_peca("X"))
        self.assertEqual(result, "[X]")

    def test_peca_para_inteiro(self):
        result = target.peca_para_inteiro(target.cria_peca(" "))

        self.assertEqual(result, 0)

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

    def test_obter_ganhador(self):
        data = target.tuplo_para_tabuleiro(
            ((0, 1, -1), (-0, 1, -1), (1, 0, -1)))

        result = target.peca_para_str(target.obter_ganhador(data))

        self.assertEqual(result, "[O]")

    def test_obter_posicoes_livres(self):
        data = target.tuplo_para_tabuleiro(
            ((0, 1, -1), (-0, 1, -1), (1, 0, -1)))

        result = tuple(
            target.posicao_para_str(p) for p in target.obter_posicoes_livres(data)
        )

        self.assertEqual(result, ("a1", "a2", "b3"))

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
