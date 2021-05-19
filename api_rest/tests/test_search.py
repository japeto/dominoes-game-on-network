import copy
import dominoes
import random
import unittest

class TestSearch(unittest.TestCase):
    def test_make_moves(self):
        game1 = dominoes.Game.new()

        for vm, (m, g) in zip(game1.valid_moves, dominoes.search.make_moves(game1)):
            self.assertEqual(vm, m)

            self.assertEqual(g.board.left_end(), m[0].first)
            self.assertEqual(g.board.right_end(), m[0].second)
            self.assertEqual(len(g.board), 1)
            self.assertEqual(len(g.hands[0]), 6)
            self.assertEqual(len(g.hands[1]), 7)
            self.assertEqual(len(g.hands[2]), 7)
            self.assertEqual(len(g.hands[3]), 7)
            self.assertEqual(g.moves[0], m)
            for p in g.moves[1:]:
                self.assertIsNone(p)
            self.assertIsNotNone(g.turn)
            self.assertTrue(bool(g.valid_moves))
            self.assertEqual(g.starting_player, 0)
            self.assertIsNone(g.result)

        game2 = dominoes.Game.new()
        game2.result = True

        self.assertEqual(list(dominoes.search.make_moves(game2)), [])

        game3 = dominoes.Game.new()
        game3_copy = copy.deepcopy(game3)

        # there is a small chance that the valid moves are already
        # sorted in bota gorda order, in which case this won't
        # test anything interesting. this test suite gets run
        # often enough that the danger is negligible.
        dominoes.players.bota_gorda(game3_copy)

        for vm, (m, g) in zip(game3_copy.valid_moves,
                              dominoes.search.make_moves(game3, dominoes.players.bota_gorda)):
            self.assertEqual(vm, m)

            self.assertEqual(g.board.left_end(), m[0].first)
            self.assertEqual(g.board.right_end(), m[0].second)
            self.assertEqual(len(g.board), 1)
            self.assertEqual(len(g.hands[0]), 6)
            self.assertEqual(len(g.hands[1]), 7)
            self.assertEqual(len(g.hands[2]), 7)
            self.assertEqual(len(g.hands[3]), 7)
            self.assertEqual(g.moves[0], m)
            for p in g.moves[1:]:
                self.assertIsNone(p)
            self.assertIsNotNone(g.turn)
            self.assertTrue(bool(g.valid_moves))
            self.assertEqual(g.starting_player, 0)
            self.assertIsNone(g.result)

    def test_alphabeta(self):
        g1 = dominoes.Game.new()
        g1.result = dominoes.Result(0, True, 10)

        self.assertEqual(([], 10), dominoes.search.alphabeta(g1))

        g2 = dominoes.Game.new()
        g2.result = dominoes.Result(1, True, -10)

        self.assertEqual(([], -10), dominoes.search.alphabeta(g2))

        d1 = dominoes.Domino(7, 0)
        d2 = dominoes.Domino(0, 0)
        d3 = dominoes.Domino(0, 1)
        d4 = dominoes.Domino(0, 2)
        d5 = dominoes.Domino(0, 3)
        d6 = dominoes.Domino(0, 4)
        d7 = dominoes.Domino(0, 5)
        d8 = dominoes.Domino(0, 6)
        d9 = dominoes.Domino(0, 8)
        d10 = dominoes.Domino(1, 9)
        d11 = dominoes.Domino(2, 10)
        d12 = dominoes.Domino(3, 11)
        d13 = dominoes.Domino(4, 12)
        d14 = dominoes.Domino(5, 13)
        d15 = dominoes.Domino(6, 14)

        h1 = dominoes.Hand([d1, d2])
        h2 = [d2, d3, d4, d5, d6, d7, d8]
        random.shuffle(h2)
        h2 = dominoes.Hand(h2)
        h3 = [d9, d10, d11, d12, d13, d14, d15]
        random.shuffle(h3)
        h3 = dominoes.Hand(h3)
        h4 = dominoes.Hand([d2])

        g3 = dominoes.Game.new(starting_player=0)
        g3.hands = [h1, h2, h3, h4]
        g3.make_move(d1, True)

        self.assertEqual(([(d2, False), (d9, False)], -111),
                         dominoes.search.alphabeta(g3))

        h5 = dominoes.Hand([d2])
        h6 = dominoes.Hand([d1, d2])
        h7 = [d2, d3, d4, d5, d6, d7, d8]
        random.shuffle(h7)
        h7 = dominoes.Hand(h7)
        h8 = [d9, d10, d11, d12, d13, d14, d15]
        random.shuffle(h8)
        h8 = dominoes.Hand(h8)

        g4 = dominoes.Game.new(starting_player=1)
        g4.hands = [h5, h6, h7, h8]
        g4.make_move(d1, True)

        self.assertEqual(([(d2, False), (d9, False)], 111),
                         dominoes.search.alphabeta(g4))

        h9 = dominoes.Hand([d1, d2])
        h10 = dominoes.Hand([d2, d3])
        h11 = dominoes.Hand([d9, d10, d3])
        h12 = dominoes.Hand([d2])

        g5 = dominoes.Game.new(starting_player=0)
        g5.hands = [h9, h10, h11, h12]
        g5.make_move(d1, True)

        cp1 = dominoes.players.counter()

        self.assertEqual(([(d2, False), (d9, False)], -12),
                         dominoes.search.alphabeta(g5, player=cp1))

        self.assertEqual(cp1.count, 4)

        h13 = dominoes.Hand([d2])
        h14 = dominoes.Hand([d1, d2])
        h15 = dominoes.Hand([d2, d3])
        h16 = dominoes.Hand([d9, d10, d3])

        g6 = dominoes.Game.new(starting_player=1)
        g6.hands = [h13, h14, h15, h16]
        g6.make_move(d1, True)

        cp2 = dominoes.players.counter()

        self.assertEqual(([(d2, False), (d9, False)], 12),
                         dominoes.search.alphabeta(g6, player=cp2))

        self.assertEqual(cp2.count, 4)

        h17 = dominoes.Hand([d1, d2])
        h18 = dominoes.Hand([d2, d3])
        h19 = dominoes.Hand([d9, d3, d10])
        h20 = dominoes.Hand([d2])

        g7 = dominoes.Game.new(starting_player=0)
        g7.hands = [h17, h18, h19, h20]
        g7.make_move(d1, True)

        def d10_before_d3(game):
            if game.valid_moves == ((d3, False), (d10, False)):
                game.valid_moves = ((d10, False), (d3, False))

        cp3 = dominoes.players.counter(d10_before_d3)

        self.assertEqual(([(d2, False), (d9, False)], -12),
                         dominoes.search.alphabeta(g7, player=cp3))

        self.assertEqual(cp3.count, 4)

        h21 = dominoes.Hand([d2])
        h22 = dominoes.Hand([d1, d2])
        h23 = dominoes.Hand([d2, d3])
        h24 = dominoes.Hand([d9, d3, d10])

        g8 = dominoes.Game.new(starting_player=1)
        g8.hands = [h21, h22, h23, h24]
        g8.make_move(d1, True)

        cp4 = dominoes.players.counter(d10_before_d3)

        self.assertEqual(([(d2, False), (d9, False)], 12),
                         dominoes.search.alphabeta(g8, player=cp4))

        self.assertEqual(cp4.count, 4)

if __name__ == '__main__':
    unittest.main()
