import unittest
import sys
import importlib
import os
from io import StringIO

target = importlib.import_module(sys.argv[1])


class SomeTest(unittest.TestCase):
    def test_example(self):
        """
        Example test
        """
        result = target.some_function()
        self.assertEqual(result, True)


class TestPosicoesIguais(unittest.TestCase):
    def test_posicoes_iguais(self):
        """
        posicoes_iguais(criar_posicao('a','2'),criar_posicao('b','3')) = False
        """
        data1 = target.cria_posicao("a", "2")
        data2 = target.cria_posicao("b", "3")

        result = target.posicoes_iguais(data1, data2)

        self.assertEqual(result, False)


class TestPosicaoParaStr(unittest.TestCase):
    def test_posicao_para_str(self):
        """
        posicao_para_str(cria_posicao("b", "3")) = 'a2'
        """
        data = target.cria_posicao("b", "3")

        result = target.posicao_para_str(data)

        self.assertEqual(result, "a2")


class TestObterPosicaoesAdjacentes(unittest.TestCase):
    def test_obter_posicoes_adjacentes(self):
        """
        posicao = cria_posicao('b', '3')
        tuple(posicao_para_str(p) for p in obter_posicoes_adjacentes(posicao)) = ('b2', 'a3', 'c3')
        """
        data1 = target.cria_posicao("a", "2")

        result = tuple(
            target.posicao_para_str(p) for p in target.obter_posicoes_adjacentes(data1)
        )

        self.assertEqual(result, ("b2", "a3", "c3"))


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
        result = target.pecas_iguais(target.cria_peca("X"), target.cria_peca("O"))

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

        result = target.tabuleiro_para_str(target.coloca_peca(data1, data2, data3))

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

        result = target.tabuleiro_para_str(target.move_peca(data4, data3, data5))

        self.assertEqual(
            result,
            "   a   b   c\n1 [ ]-[X]-[ ]\n   | \\ | / |\n2 [ ]-[ ]-[ ]\n   | / | \\ |\n3 [ ]-[ ]-[ ]",
        )


class TestObterGanhador(unittest.TestCase):
    def test_obter_ganhador(self):
        data = target.tuplo_para_tabuleiro(((0, 1, -1), (-0, 1, -1), (1, 0, -1)))

        result = target.peca_para_str(target.obter_ganhador(data))

        self.assertEqual(result, "[O]")


class TestObterPosicoesLivres(unittest.TestCase):
    def test_obter_posicoes_livres(self):
        data = target.tuplo_para_tabuleiro(((0, 1, -1), (-0, 1, -1), (1, 0, -1)))

        result = tuple(
            target.posicao_para_str(p) for p in target.obter_posicoes_livres(data)
        )

        self.assertEqual(result, ("a1", "a2", "b3"))


class TestObterVetor(unittest.TestCase):
    def test_obter_vetor(self):
        data = target.tuplo_para_tabuleiro(((0, 1, -1), (-0, 1, -1), (1, 0, -1)))

        result = tuple(
            target.peca_para_str(peca) for peca in target.obter_vetor(data, "a")
        )

        self.assertEqual(("[ ]", "[ ]", "[X]"))

    def test_obter_vetor(self):
        data = target.tuplo_para_tabuleiro(((0, 1, -1), (-0, 1, -1), (1, 0, -1)))

        result = tuple(
            target.peca_para_str(peca) for peca in target.obter_vetor(data, "2")
        )

        self.assertEqual(("[ ]", "[X]", "[O]"))


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])
