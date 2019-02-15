from DoubleCard import DoubleCard


def test1():
    with open('test_cases/diagonal_open_win.txt') as f:
        game = DoubleCard()
        game.verbose_output = False
        game.play(input_file=f)


def test2():
    with open('test_cases/24_valid_moves_no_win.txt') as f:
        game = DoubleCard()
        game.verbose_output = False
        game.play(input_file=f)


if __name__ == "__main__":
    print("Starting Test")
    test2()
    print('Testing Over')
