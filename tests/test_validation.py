import tempfile
import unittest
from pathlib import Path

from sequence_design.validation import (
    validate_czcs_csv,
    validate_gcs_index_csv,
    validate_known_zcps,
    validate_reference_datasets,
)


ROOT = Path(__file__).resolve().parents[1]
CZCS_ROOT = ROOT / "data" / "reference" / "czcs"


class ValidationTests(unittest.TestCase):
    def test_known_zcp_results(self) -> None:
        results = validate_known_zcps()
        self.assertEqual(
            [(result.expected_zone, result.measured_zone) for result in results],
            [(18, 18), (26, 26), (21, 21)],
        )
        self.assertTrue(all(result.valid for result in results))

    def test_archived_dataset_regression_counts(self) -> None:
        results = validate_reference_datasets(CZCS_ROOT)
        observed = {
            result.length: (result.valid_rows, result.rows)
            for result in results
        }
        self.assertEqual(
            observed,
            {
                2: (40, 40),
                3: (176, 176),
                4: (128, 128),
                5: (448, 448),
                6: (224, 224),
                7: (10, 10),
                8: (24, 24),
                9: (0, 294),
                10: (0, 233),
                11: (4, 4),
            },
        )

    def test_malformed_rows_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "length_2_CZCS.csv"
            path.write_text("0,0,0,0,1,0,0,1\n0,2\n", encoding="utf-8")
            result = validate_czcs_csv(path)
        self.assertEqual(result.rows, 2)
        self.assertEqual(result.valid_rows, 1)
        self.assertEqual(result.malformed_rows, 1)

    def test_archived_gcs_index_table_is_structurally_valid(self) -> None:
        result = validate_gcs_index_csv(
            ROOT / "data" / "reference" / "gcs" / "length_7_GCS.csv"
        )
        self.assertTrue(result.is_valid)
        self.assertEqual(result.rows, 6798)
        self.assertEqual(result.unique_rows, 6798)
        self.assertEqual((result.minimum_index, result.maximum_index), (1, 64))


if __name__ == "__main__":
    unittest.main()
