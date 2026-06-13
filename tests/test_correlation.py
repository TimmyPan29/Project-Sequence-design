import unittest

from sequence_design.correlation import (
    aperiodic_autocorrelation,
    aperiodic_cross_correlation,
    sum_correlations,
    to_bipolar,
)


class CorrelationTests(unittest.TestCase):
    def test_binary_and_bipolar_inputs_are_equivalent(self) -> None:
        binary = (0, 1, 1, 0)
        bipolar = (-1, 1, 1, -1)
        self.assertEqual(to_bipolar(binary), bipolar)
        self.assertEqual(
            aperiodic_autocorrelation(binary),
            aperiodic_autocorrelation(bipolar),
        )

    def test_autocorrelation_matches_hand_calculation(self) -> None:
        self.assertEqual(
            aperiodic_autocorrelation((1, 1, -1)),
            (3, 0, -1),
        )

    def test_cross_correlation_orientation_matches_legacy_mex(self) -> None:
        first = (1, -1, 1)
        second = (1, 1, -1)
        self.assertEqual(
            aperiodic_cross_correlation(first, second),
            (-1, 0, 1),
        )

    def test_sum_correlations_rejects_mismatched_lengths(self) -> None:
        with self.assertRaises(ValueError):
            sum_correlations((1, 2), (1,))

    def test_invalid_alphabet_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            to_bipolar((0, 2, 1))


if __name__ == "__main__":
    unittest.main()

