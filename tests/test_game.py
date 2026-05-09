import io
from contextlib import redirect_stdout

from trivia.game import Game
from trivia.game_old import GameOld


class JavaRandom:
    def __init__(self, seed):
        self.seed = (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)

    def next(self, bits):
        self.seed = (self.seed * 0x5DEECE66D + 0xB) & ((1 << 48) - 1)
        return self.seed >> (48 - bits)

    def next_int(self, bound):
        if bound <= 0:
            raise ValueError("bound must be positive")

        if (bound & (bound - 1)) == 0:
            return (bound * self.next(31)) >> 31

        while True:
            bits = self.next(31)
            value = bits % bound
            if bits - value + (bound - 1) >= 0:
                return value


def extract_output(random_generator, game):
    output = io.StringIO()

    with redirect_stdout(output):
        game.add("Chet")
        game.add("Pat")
        game.add("Sue")

        not_a_winner = False

        while True:
            game.roll(random_generator.next_int(5) + 1)

            if random_generator.next_int(9) == 7:
                not_a_winner = game.wrongAnswer()
            else:
                not_a_winner = game.handleCorrectAnswer()

            if not not_a_winner:
                break

    return output.getvalue()


def test_game_matches_golden_master():
    for seed in range(1, 10_000):
        expected_output = extract_output(JavaRandom(seed), GameOld())
        actual_output = extract_output(JavaRandom(seed), Game())

        assert expected_output == actual_output, f"Change detected for seed {seed}"


def test_one_seed_can_be_checked_manually():
    seed = 1

    expected_output = extract_output(JavaRandom(seed), GameOld())
    actual_output = extract_output(JavaRandom(seed), Game())

    assert expected_output == actual_output