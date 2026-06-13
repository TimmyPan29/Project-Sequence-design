"""Reference search implementations for small reproducible experiments."""

from collections.abc import Iterator
from itertools import combinations, combinations_with_replacement

from .correlation import aperiodic_autocorrelation
from .properties import is_optimal_czcs
from .sequences import integer_to_binary_sequence, transition_sequence


def transition_candidates(
    length: int,
    transition_count: int,
    *,
    prefix: int = 1,
) -> Iterator[tuple[int, ...]]:
    """Yield sequences with a fixed zero prefix and transition count."""
    if prefix < 1 or prefix >= length:
        raise ValueError("prefix must satisfy 1 <= prefix < length")
    if transition_count < 0 or transition_count > length - prefix:
        raise ValueError("invalid transition count")

    available = range(prefix + 1, length + 1)
    for positions in combinations(available, transition_count):
        yield transition_sequence(length, positions)


def find_gcs_indices(
    length: int,
    *,
    set_size: int = 4,
) -> list[tuple[int, ...]]:
    """Exhaustively find complementary sets for small sequence lengths.

    Returned indices are zero-based integer encodings of the binary sequences.
    """
    if length < 1:
        raise ValueError("length must be positive")
    if set_size < 2:
        raise ValueError("set_size must be at least two")

    sequences = [
        integer_to_binary_sequence(value, length) for value in range(2**length)
    ]
    autocorrelations = [
        aperiodic_autocorrelation(sequence) for sequence in sequences
    ]
    results: list[tuple[int, ...]] = []
    for indices in combinations_with_replacement(range(len(sequences)), set_size):
        if all(
            sum(autocorrelations[index][lag] for index in indices) == 0
            for lag in range(1, length)
        ):
            results.append(indices)
    return results


def find_optimal_czcs(length: int) -> list[tuple[tuple[int, ...], ...]]:
    """Find optimal four-sequence CZCSs for small lengths."""
    sequences = [
        integer_to_binary_sequence(value, length) for value in range(2**length)
    ]
    results = []
    for indices in find_gcs_indices(length):
        candidate = tuple(sequences[index] for index in indices)
        if is_optimal_czcs(candidate):
            results.append(candidate)
    return results

