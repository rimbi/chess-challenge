from unittest import TestCase
from main import get_unique_configurations, Knight, King, Queen, Rook, Bishop


class TestGet(TestCase):
    def test_get_unique_configurations_3_3(self):
        results = get_unique_configurations(3, 3, {'k': 2, 'r': 1})
        expected = [set([(0, 0), (0, 2), (2, 1)]),
                    set([(1, 2), (2, 0), (0, 0)]),
                    set([(0, 1), (2, 0), (2, 2)]),
                    set([(1, 0), (0, 2), (2, 2)])]
        self.assertEqual(expected, results)

    def test_get_unique_configurations_4_4(self):
        results = get_unique_configurations(4, 4, {'r': 2, 'n': 4})
        expected = [set([(1, 3), (3, 3), (2, 2), (3, 1), (1, 1), (0, 0)]),
                    set([(2, 0), (0, 0), (3, 3), (2, 2), (0, 2), (1, 1)]),
                    set([(2, 0), (1, 3), (2, 2), (3, 1), (0, 2), (0, 0)]),
                    set([(0, 1), (1, 2), (3, 2), (2, 3), (3, 0), (1, 0)]),
                    set([(0, 1), (3, 2), (2, 3), (0, 3), (1, 0), (2, 1)]),
                    set([(0, 1), (1, 2), (2, 3), (3, 0), (0, 3), (2, 1)]),
                    set([(2, 0), (1, 3), (3, 3), (3, 1), (0, 2), (1, 1)]),
                    set([(1, 2), (3, 2), (3, 0), (0, 3), (1, 0), (2, 1)])]
        self.assertEqual(expected, results)


class TestKnight(TestCase):
    def test_get_targets(self):
        piece = Knight()
        m, n = 3, 3
        self.assertEqual({(1, 2), (2, 1)}, piece.get_targets(m, n, 0, 0))
        self.assertEqual(set(), piece.get_targets(m, n, 1, 1))

        m, n = 4, 4
        self.assertEqual({(3, 0), (0, 3), (2, 3), (3, 2)},
                         piece.get_targets(m, n, 1, 1))


class TestKing(TestCase):
    def test_get_targets(self):
        piece = King()

        m, n = 3, 3
        self.assertEqual({(0, 1), (1, 1), (1, 0)},
                         piece.get_targets(m, n, 0, 0))
        self.assertEqual(
            {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)},
            piece.get_targets(m, n, 1, 1))


class TestQueen(TestCase):
    def test_get_targets(self):
        piece = Queen()

        m, n = 3, 3
        self.assertEqual({(0, 1), (1, 1), (0, 2), (1, 0), (2, 0), (2, 2)},
                         piece.get_targets(m, n, 0, 0))
        self.assertEqual(
            {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)},
            piece.get_targets(m, n, 1, 1))


class TestRook(TestCase):
    def test_get_targets(self):
        piece = Rook()

        m, n = 3, 3
        self.assertEqual({(0, 1), (0, 2), (1, 0), (2, 0)},
                         piece.get_targets(m, n, 0, 0))
        self.assertEqual({(0, 1), (1, 0), (1, 2), (2, 1)},
                         piece.get_targets(m, n, 1, 1))


class TestBishop(TestCase):
    def test_get_targets(self):
        piece = Bishop()

        m, n = 3, 3
        self.assertEqual({(1, 1), (2, 2)}, piece.get_targets(m, n, 0, 0))
        self.assertEqual({(0, 0), (2, 0), (0, 2), (2, 2)},
                         piece.get_targets(m, n, 1, 1))
