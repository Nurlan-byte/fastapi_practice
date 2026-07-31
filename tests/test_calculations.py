import pytest
from app.calculations import add, subtract, multiply, divide

#@pytest.fixture
@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16),
    (-1, -1, -2)
])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected
    
def test_sunbtract():
    assert subtract(9, 4) == 5
    