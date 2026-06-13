import unittest

from sequence_design.sequences import (
    integer_to_binary_sequence,
    transition_positions,
    transition_sequence,
)


class SequenceGenerationTests(unittest.TestCase):
    def test_transition_sequence_reproduces_suffix_toggling(self) -> None:
        self.assertEqual(
            transition_sequence(7, (2, 5, 7)),
            (0, 1, 1, 1, 0, 0, 1),
        )

    def test_transition_positions_round_trip(self) -> None:
        positions = (3, 5, 8)
        sequence = transition_sequence(9, positions)
        self.assertEqual(transition_positions(sequence), positions)

    def test_integer_conversion_is_most_significant_bit_first(self) -> None:
        self.assertEqual(integer_to_binary_sequence(5, 4), (0, 1, 0, 1))

    def test_duplicate_transition_positions_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            transition_sequence(5, (2, 2))


if __name__ == "__main__":
    unittest.main()

