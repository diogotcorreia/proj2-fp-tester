import unittest
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
                     ('c', 2), ('aa', '-2'), ('b', 3.0), ('c', '11'))

        for case in testcases:
            with self.assertRaises(ValueError) as ctx:
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
        isto é, "original == copia" tem de retornar False.
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
        for case in (True, False, 34, 'fail', 43.543, {'c': 'a', 'l': 4}, ['z', '4'], ('d', '1')):
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
