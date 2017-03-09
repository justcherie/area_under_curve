#!python3
import unittest
import __init__ as auc

class BoundsOK(unittest.TestCase):
    """Test class for Bounds class"""
    def test_ok(self):
        """run test method"""
        bounds_ok = auc.Bounds(2, 4, .1)
        #print(bounds_ok)
        assert bounds_ok.lower_bound == 2
        assert bounds_ok.upper_bound == 4
        assert bounds_ok.step_size == .1
        assert len(bounds_ok.full_range) == 21
        #print(bounds_ok.full_range)

    @unittest.expectedFailure
    def test_bad_step_size(self):
        """run test method"""
        auc.Bounds(2, 4, 0)

    @unittest.expectedFailure
    def test_bad_bounds(self):
        """run test method"""
        auc.Bounds(2, 2, 1)

if __name__ == "__main__":
    unittest.main()
