from game2048 import Game2048, merge_line, parse_direction


def test_merge_line_combines_once_per_pair() -> None:
    merged, score_gain, changed = merge_line([2, 2, 2, 2])
    assert merged == [4, 4, 0, 0]
    assert score_gain == 8
    assert changed is True


def test_move_left_updates_score_without_spawning() -> None:
    game = Game2048(seed=1)
    game.board = [
        [2, 0, 2, 4],
        [0, 4, 4, 0],
        [0, 0, 0, 0],
        [2, 2, 2, 0],
    ]

    result = game.move("left", spawn=False)

    assert result.changed is True
    assert result.score_gain == 12
    assert game.score == 12
    assert game.board == [
        [4, 4, 0, 0],
        [8, 0, 0, 0],
        [0, 0, 0, 0],
        [4, 2, 0, 0],
    ]


def test_move_up_merges_columns_without_double_merge() -> None:
    game = Game2048(seed=1)
    game.board = [
        [2, 2, 0, 0],
        [2, 0, 0, 0],
        [4, 2, 0, 0],
        [4, 0, 0, 0],
    ]

    result = game.move("up", spawn=False)

    assert result.changed is True
    assert result.score_gain == 12
    assert game.board == [
        [4, 4, 0, 0],
        [8, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]


def test_parse_direction_handles_shortcuts_and_words() -> None:
    assert parse_direction("w") == "up"
    assert parse_direction("LEFT") == "left"
    assert parse_direction("nope") is None


def test_can_move_detects_locked_board() -> None:
    game = Game2048(seed=1)
    game.board = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]

    assert game.can_move() is False
