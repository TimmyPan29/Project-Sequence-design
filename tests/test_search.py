import unittest

from sequence_design.search import (
    find_gcs_indices,
    find_optimal_czcs,
    transition_candidates,
)


class SearchTests(unittest.TestCase):
    def test_transition_candidate_count(self) -> None:
        candidates = list(transition_candidates(6, 2, prefix=2))
        self.assertEqual(len(candidates), 6)
        self.assertEqual(len(set(candidates)), 6)

    def test_small_exhaustive_search_is_reproducible(self) -> None:
        self.assertEqual(len(find_gcs_indices(2)), 9)
        self.assertEqual(len(find_optimal_czcs(2)), 2)


if __name__ == "__main__":
    unittest.main()

