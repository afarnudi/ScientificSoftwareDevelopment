def test_uppercase():
    assert "loud noises".upper() == "LOUD NOISES"

def test_reversed():
    assert list(reversed([1, 2, 3, 4])) == [4, 3, 2, 1]

import numpy as np

def test_squaring():
	'Test calculating the element-wise square of an array'
	a = np.array([1., 2., 3.])
	a_squared = np.array([1., 4., 9.])
	np.testing.assert_array_almost_equal(a**2, a_squared)

def test_sum():
	a = np.array([1.2, -1.0])
	assert a.sum() == 0.2
	# np.testing.assert_approx_equal(a.sum(), 0.2) # Try this instead!

