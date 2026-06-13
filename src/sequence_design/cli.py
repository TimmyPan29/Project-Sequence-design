"""Command-line interface for reproducible validation and demonstrations."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .correlation import aperiodic_autocorrelation
from .properties import zero_correlation_zone
from .validation import (
    validate_gcs_index_csv,
    validate_known_zcps,
    validate_reference_datasets,
)

KNOWN_CZCS_ANOMALIES = {9: 294, 10: 233}


def _parse_sequence(value: str) -> tuple[int, ...]:
    compact = value.replace(",", "").replace(" ", "")
    if not compact:
        raise argparse.ArgumentTypeError("sequence must not be empty")
    mapping = {"0": 0, "1": 1, "+": 1, "-": -1}
    try:
        return tuple(mapping[character] for character in compact)
    except KeyError as error:
        raise argparse.ArgumentTypeError(
            "sequence must contain only 0/1, +/- and optional separators"
        ) from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sequence-design",
        description="Binary ZCP, GCP, and CZCS design utilities",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser(
        "validate",
        help="validate known ZCPs and archived CZCS datasets",
    )
    validate.add_argument(
        "--data-root",
        type=Path,
        default=Path("data/reference/czcs"),
        help="directory containing length_*_CZCS.csv files",
    )
    validate.add_argument(
        "--gcs-index-file",
        type=Path,
        default=Path("data/reference/gcs/length_7_GCS.csv"),
        help="archived GCS index table to audit structurally",
    )

    acf = subparsers.add_parser("acf", help="compute positive-lag AACF")
    acf.add_argument("sequence", type=_parse_sequence)

    zcp = subparsers.add_parser("zcp", help="measure a sequence pair's ZCZ width")
    zcp.add_argument("first", type=_parse_sequence)
    zcp.add_argument("second", type=_parse_sequence)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "acf":
        print(" ".join(str(value) for value in aperiodic_autocorrelation(args.sequence)))
        return 0
    if args.command == "zcp":
        print(zero_correlation_zone(args.first, args.second))
        return 0
    if args.command == "validate":
        return _run_validation(args.data_root, args.gcs_index_file)
    raise AssertionError(f"unhandled command: {args.command}")


def _run_validation(data_root: Path, gcs_index_file: Path) -> int:
    print("Known ZCP fixtures")
    zcp_results = validate_known_zcps()
    for result in zcp_results:
        status = "PASS" if result.valid else "FAIL"
        print(
            f"  {status} {result.name}: "
            f"expected Z={result.expected_zone}, measured Z={result.measured_zone}"
        )

    print("\nArchived optimal CZCS datasets")
    dataset_results = validate_reference_datasets(data_root)
    for result in dataset_results:
        known_issue = (
            result.length in KNOWN_CZCS_ANOMALIES
            and result.invalid_rows == KNOWN_CZCS_ANOMALIES[result.length]
            and result.malformed_rows == 0
        )
        status = "PASS" if result.is_valid else "KNOWN ISSUE" if known_issue else "FAIL"
        print(
            f"  {status} L={result.length}: "
            f"{result.valid_rows}/{result.rows} valid, "
            f"{result.malformed_rows} malformed"
        )

    print("\nArchived GCS index dataset")
    gcs_result = validate_gcs_index_csv(gcs_index_file)
    gcs_status = "PASS" if gcs_result.is_valid else "FAIL"
    print(
        f"  {gcs_status} {gcs_result.path.name}: "
        f"{gcs_result.rows} rows, {gcs_result.unique_rows} unique, "
        f"index range {gcs_result.minimum_index}..{gcs_result.maximum_index}"
    )
    print("  NOTE Mathematical replay requires the missing candidate-index map.")

    datasets_expected = all(
        result.is_valid
        or (
            result.length in KNOWN_CZCS_ANOMALIES
            and result.invalid_rows == KNOWN_CZCS_ANOMALIES[result.length]
            and result.malformed_rows == 0
        )
        for result in dataset_results
    )
    return 0 if (
        all(result.valid for result in zcp_results)
        and datasets_expected
        and gcs_result.is_valid
    ) else 1
