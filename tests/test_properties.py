import unittest

from sequence_design.properties import (
    cyclic_summed_cross_correlation,
    is_gcs,
    is_optimal_czcs,
    is_zcp,
    zero_correlation_zone,
)


class PropertyTests(unittest.TestCase):
    def test_length_two_golay_pair(self) -> None:
        first = (1, 1)
        second = (1, -1)
        self.assertTrue(is_gcs((first, second)))
        self.assertTrue(is_zcp(first, second, 2))
        self.assertEqual(zero_correlation_zone(first, second), 2)

    def test_known_length_two_optimal_czcs(self) -> None:
        sequences = (
            (0, 0),
            (0, 0),
            (1, 0),
            (0, 1),
        )
        self.assertTrue(is_optimal_czcs(sequences))
        self.assertEqual(cyclic_summed_cross_correlation(sequences), (0, 0))

    def test_wrong_cross_correlation_order_is_not_czcs(self) -> None:
        sequences = (
            (0, 0),
            (0, 0),
            (0, 1),
            (1, 0),
        )
        self.assertFalse(is_optimal_czcs(sequences))


if __name__ == "__main__":
    unittest.main()
