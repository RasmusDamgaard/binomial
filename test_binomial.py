from binomial import optionPrice, payoff, plotTree
import numpy as np
import pytest


def test_price():
    assert optionPrice(50, 52, 0.3, 0.05, 3, 4, "Put", "A") == "8.2724"
    assert optionPrice(50, 45, 0.3, 0.05, 3, 4, "Call", "E") == "15.8216"


def test_payoff():
    assert payoff(60, 40, Type="Call") == 20
    assert payoff(50, 20, Type="Put") == 0


def test_plot():
    with pytest.raises(TypeError):
        plotTree(1,1,1)
    with pytest.raises(IndexError):
        plotTree(np.zeros((2,2)),np.zeros((1,1)),2)

