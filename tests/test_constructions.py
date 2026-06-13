import unittest

from sequence_design.constructions import kronecker_zcp
from sequence_design.properties import zero_correlation_zone


class ConstructionTests(unittest.TestCase):
    def test_legacy_length_34_construction(self) -> None:
        first_kernel = (
            -1, -1, -1, -1, -1, -1, -1, 1, -1,
            1, 1, 1, -1, -1, -1, 1, 1,
        )
        second_kernel = (
            -1, -1, 1, -1, 1, 1, -1, -1, 1,
            1, -1, 1, -1, 1, -1, -1, 1,
        )
        first, second = kronecker_zcp(first_kernel, second_kernel)
        self.assertEqual(len(first), 34)
        self.assertEqual(zero_correlation_zone(first, second), 18)

    def test_legacy_length_36_construction(self) -> None:
        first_kernel = (
            -1, -1, -1, -1, 1, -1, -1, 1, -1,
            -1, 1, -1, -1, -1, 1, 1, 1, 1,
        )
        second_kernel = (
            -1, 1, 1, 1, -1, -1, -1, 1, -1,
            1, -1, 1, 1, -1, 1, 1, 1, -1,
        )
        first, second = kronecker_zcp(first_kernel, second_kernel)
        self.assertEqual(len(first), 36)
        self.assertEqual(zero_correlation_zone(first, second), 26)


if __name__ == "__main__":
    unittest.main()

