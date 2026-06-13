"""Definitions and predicates for complementary sequence families."""

from collections.abc import Sequence

from .correlation import (
    NumericSequence,
    aperiodic_autocorrelation,
    aperiodic_cross_correlation,
    sum_correlations,
    to_bipolar,
)


def summed_autocorrelation(sequences: Sequence[NumericSequence]) -> tuple[int, ...]:
    """Return the sum of all sequence autocorrelations."""
    if not sequences:
        raise ValueError("at least one sequence is required")
    return sum_correlations(
        *(aperiodic_autocorrelation(sequence) for sequence in sequences)
    )


def cyclic_summed_cross_correlation(
    sequences: Sequence[NumericSequence],
) -> tuple[int, ...]:
    """Sum cross-correlations of adjacent sequences, including last-to-first."""
    if len(sequences) < 2:
        raise ValueError("at least two sequences are required")
    normalized = tuple(to_bipolar(sequence) for sequence in sequences)
    return sum_correlations(
        *(
            aperiodic_cross_correlation(
                normalized[index],
                normalized[(index + 1) % len(normalized)],
            )
            for index in range(len(normalized))
        )
    )


def zero_correlation_zone(
    first: NumericSequence,
    second: NumericSequence,
) -> int:
    """Return ``Z`` where summed AACF is zero for lags ``1 <= u < Z``."""
    summed = summed_autocorrelation((first, second))
    zone = 1
    while zone < len(summed) and summed[zone] == 0:
        zone += 1
    return zone


def is_zcp(
    first: NumericSequence,
    second: NumericSequence,
    zone: int,
) -> bool:
    """Return whether two sequences form an ``(L, Z)`` ZCP."""
    first_values = to_bipolar(first)
    second_values = to_bipolar(second)
    if len(first_values) != len(second_values):
        return False
    if zone < 1 or zone > len(first_values):
        raise ValueError("zone must be within [1, sequence length]")
    summed = summed_autocorrelation((first_values, second_values))
    return all(value == 0 for value in summed[1:zone])


def is_gcs(sequences: Sequence[NumericSequence]) -> bool:
    """Return whether the sequences form a full complementary set."""
    summed = summed_autocorrelation(sequences)
    return all(value == 0 for value in summed[1:])


def is_optimal_czcs(sequences: Sequence[NumericSequence]) -> bool:
    """Reproduce the archived final-project optimal CZCS criterion.

    The implementation requires a full complementary set and zero cyclic
    summed positive-lag ACCF at every lag, including lag zero.
    """
    if len(sequences) != 4:
        return False
    return is_gcs(sequences) and all(
        value == 0 for value in cyclic_summed_cross_correlation(sequences)
    )

