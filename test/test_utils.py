from src import utils


def test_add_():
    assert utils.add_(2, 3) == 5
    assert utils.add_(0, 0) == 0
    assert utils.add_(-5, 5) == 0
    assert utils.add_(10, -3) == 7
