import unittest

from game2048 import Game2048, merge_line, parse_direction


class Game2048Tests(unittest.TestCase):
    def test_merge_line_combines_once_per_pair(self) -> None:
        merged, score_gain, changed = merge_line([2, 2, 2, 2])
        self.assertEqual(merged, [4, 4, 0, 0])
        self.assertEqual(score_gain, 8)
        self.assertTrue(changed)

    def test_move_left_updates_score_without_spawning(self) -> None:
        game = Game2048(seed=1)
        game.board = [
            [2, 0, 2, 4],
            [0, 4, 4, 0],
            [0, 0, 0, 0],
            [2, 2, 2, 0],
        ]

        result = game.move("left", spawn=False)

        self.assertTrue(result.changed)
        self.assertEqual(result.score_gain, 16)
        self.assertEqual(game.score, 16)
        self.assertEqual(
            game.board,
            [
                [4, 4, 0, 0],
                [8, 0, 0, 0],
                [0, 0, 0, 0],
                [4, 2, 0, 0],
            ],
        )

    def test_move_up_merges_columns_without_double_merge(self) -> None:
        game = Game2048(seed=1)
        game.board = [
            [2, 2, 0, 0],
            [2, 0, 0, 0],
            [4, 2, 0, 0],
            [4, 0, 0, 0],
        ]

        result = game.move("up", spawn=False)

        self.assertTrue(result.changed)
        self.assertEqual(result.score_gain, 16)
        self.assertEqual(
            game.board,
            [
                [4, 4, 0, 0],
                [8, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ],
        )

    def test_parse_direction_handles_shortcuts_and_words(self) -> None:
        self.assertEqual(parse_direction("w"), "up")
        self.assertEqual(parse_direction("LEFT"), "left")
        self.assertIsNone(parse_direction("nope"))

    def test_can_move_detects_locked_board(self) -> None:
        game = Game2048(seed=1)
        game.board = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]

        self.assertFalse(game.can_move())


if __name__ == "__main__":
    unittest.main()
