import pytest
from factorial import factorial
@pytest.mark.parametrize("number,answer", [
    (1, 1),
    (2, 2),
    (3, 6),
    (4, 24),
    (10, 3628800),
])

def test_int_factorials(number, answer):
    assert(factorial(number)==answer)

def print_2():
    print("Hi")

def test_factorial_of_zero():
    assert(factorial(0)==1)

def test_factorial_negative():
    with pytest.raises(SomeError):
        factorial(-1)

