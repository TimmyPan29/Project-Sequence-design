"""Aperiodic correlation primitives used by every search and validator."""

from collections.abc import Iterable, Sequence

NumericSequence = Sequence[int] | Iterable[int]


def to_bipolar(sequence: NumericSequence) -> tuple[int, ...]:
    """Normalize a binary sequence to the bipolar alphabet ``{-1, +1}``."""
    values = tuple(int(value) for value in sequence)
    if not values:
        raise ValueError("sequence must not be empty")

    alphabet = set(values)
    if alphabet <= {0, 1}:
        return tuple(1 if value else -1 for value in values)
    if alphabet <= {-1, 1}:
        return values
    raise ValueError("sequence values must belong to {0, 1} or {-1, +1}")


def aperiodic_cross_correlation(
    first: NumericSequence,
    second: NumericSequence,
) -> tuple[int, ...]:
    """Return positive-lag aperiodic cross-correlation.

    The orientation matches the original MEX implementation:
    ``R_xy(u) = sum(x[n + u] * y[n])`` for ``u = 0, ..., L - 1``.
    """
    x = to_bipolar(first)
    y = to_bipolar(second)
    if len(x) != len(y):
        raise ValueError("sequences must have equal length")

    length = len(x)
    return tuple(
        sum(x[index + lag] * y[index] for index in range(length - lag))
        for lag in range(length)
    )


def aperiodic_autocorrelation(sequence: NumericSequence) -> tuple[int, ...]:
    """Return positive-lag aperiodic autocorrelation."""
    return aperiodic_cross_correlation(sequence, sequence)


def sum_correlations(*correlations: Sequence[int]) -> tuple[int, ...]:
    """Add equal-length correlation vectors element by element."""
    if not correlations:
        raise ValueError("at least one correlation is required")

    length = len(correlations[0])
    if any(len(correlation) != length for correlation in correlations):
        raise ValueError("correlations must have equal length")
    return tuple(sum(values) for values in zip(*correlations, strict=True))

