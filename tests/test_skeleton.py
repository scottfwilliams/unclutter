# -*- coding: utf-8 -*-

import pytest
from unclutter.skeleton import fib

__author__ = "Scott Williams"
__copyright__ = "Scott Williams"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
