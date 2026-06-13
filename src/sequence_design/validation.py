"""Validation of archived sequence datasets and known ZCP constructions."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .constructions import kronecker_zcp
from .properties import is_optimal_czcs, is_zcp, zero_correlation_zone


@dataclass(frozen=True)
class DatasetValidation:
    path: Path
    length: int
    rows: int
    valid_rows: int
    malformed_rows: int

    @property
    def invalid_rows(self) -> int:
        return self.rows - self.valid_rows

    @property
    def is_valid(self) -> bool:
        return self.invalid_rows == 0


@dataclass(frozen=True)
class ZcpValidation:
    name: str
    expected_zone: int
    measured_zone: int
    valid: bool


@dataclass(frozen=True)
class IndexDatasetValidation:
    path: Path
    rows: int
    unique_rows: int
    malformed_rows: int
    minimum_index: int | None
    maximum_index: int | None

    @property
    def is_valid(self) -> bool:
        return self.rows > 0 and self.malformed_rows == 0 and self.rows == self.unique_rows


def validate_czcs_csv(path: Path, length: int | None = None) -> DatasetValidation:
    """Validate every row as four concatenated binary sequences."""
    inferred_length = length or _length_from_name(path)
    rows = 0
    valid_rows = 0
    malformed_rows = 0

    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.reader(handle):
            rows += 1
            try:
                values = tuple(int(value) for value in row)
            except ValueError:
                malformed_rows += 1
                continue
            if len(values) != 4 * inferred_length or not set(values) <= {0, 1}:
                malformed_rows += 1
                continue
            sequences = tuple(
                values[index * inferred_length : (index + 1) * inferred_length]
                for index in range(4)
            )
            if is_optimal_czcs(sequences):
                valid_rows += 1

    return DatasetValidation(
        path=path,
        length=inferred_length,
        rows=rows,
        valid_rows=valid_rows,
        malformed_rows=malformed_rows,
    )


def validate_reference_datasets(root: Path) -> list[DatasetValidation]:
    """Validate all ``length_*_CZCS.csv`` files below a directory."""
    return [
        validate_czcs_csv(path)
        for path in sorted(root.glob("length_*_CZCS.csv"), key=_length_from_name)
    ]


def validate_gcs_index_csv(path: Path, *, set_size: int = 4) -> IndexDatasetValidation:
    """Structurally validate a GCS index table when its candidate map is absent."""
    rows = 0
    malformed_rows = 0
    parsed_rows: set[tuple[int, ...]] = set()
    indices: list[int] = []

    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.reader(handle):
            rows += 1
            try:
                values = tuple(int(value) for value in row)
            except ValueError:
                malformed_rows += 1
                continue
            if (
                len(values) != set_size
                or any(value < 1 for value in values)
                or tuple(sorted(values)) != values
            ):
                malformed_rows += 1
                continue
            parsed_rows.add(values)
            indices.extend(values)

    return IndexDatasetValidation(
        path=path,
        rows=rows,
        unique_rows=len(parsed_rows),
        malformed_rows=malformed_rows,
        minimum_index=min(indices, default=None),
        maximum_index=max(indices, default=None),
    )


def validate_known_zcps() -> list[ZcpValidation]:
    """Validate exact ZCP fixtures recovered from reports and result files."""
    fixtures: list[tuple[str, tuple[int, ...], tuple[int, ...], int]] = []

    c34 = (-1, -1, -1, -1, -1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, 1)
    d34 = (-1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, -1, -1, 1)
    first34, second34 = kronecker_zcp(c34, d34)
    fixtures.append(("Kronecker L=34", first34, second34, 18))

    c36 = (-1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1)
    d36 = (-1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1)
    first36, second36 = kronecker_zcp(c36, d36)
    fixtures.append(("Kronecker L=36", first36, second36, 26))

    first41 = (
        0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1,
        1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0,
    )
    second41 = (
        0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1,
        1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    )
    fixtures.append(("Exhaustive search L=41", first41, second41, 21))

    return [
        ZcpValidation(
            name=name,
            expected_zone=zone,
            measured_zone=zero_correlation_zone(first, second),
            valid=is_zcp(first, second, zone),
        )
        for name, first, second, zone in fixtures
    ]


def _length_from_name(path: Path) -> int:
    try:
        return int(path.stem.split("_")[1])
    except (IndexError, ValueError) as error:
        raise ValueError(f"cannot infer sequence length from {path.name}") from error
