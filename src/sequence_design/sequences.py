"""Binary sequence generation helpers."""

from collections.abc import Iterable, Sequence


def transition_sequence(
    length: int,
    positions: Iterable[int],
    *,
    start: int = 0,
) -> tuple[int, ...]:
    """Construct a binary sequence from one-indexed transition positions.

    This is the portable equivalent of ``finding_seq37.c``,
    ``finding_seq41.c``, and the archived ``finding_seqL`` MEX binary.
    """
    if length < 1:
        raise ValueError("length must be positive")
    if start not in {0, 1}:
        raise ValueError("start must be 0 or 1")

    normalized = tuple(int(position) for position in positions)
    if normalized != tuple(sorted(set(normalized))):
        raise ValueError("positions must be strictly increasing")
    if any(position < 1 or position > length for position in normalized):
        raise ValueError("positions must be within [1, length]")

    result = [start] * length
    current = start
    position_index = 0
    for index in range(1, length + 1):
        if position_index < len(normalized) and index == normalized[position_index]:
            current = 1 - current
            position_index += 1
        result[index - 1] = current
    return tuple(result)


def transition_positions(sequence: Sequence[int]) -> tuple[int, ...]:
    """Return one-indexed positions where a binary sequence changes value."""
    values = tuple(int(value) for value in sequence)
    if not values:
        raise ValueError("sequence must not be empty")
    if not set(values) <= {0, 1}:
        raise ValueError("sequence values must belong to {0, 1}")

    return tuple(
        index + 1
        for index in range(1, len(values))
        if values[index] != values[index - 1]
    )


def integer_to_binary_sequence(value: int, length: int) -> tuple[int, ...]:
    """Convert an integer to a fixed-length, most-significant-bit-first sequence."""
    if length < 1:
        raise ValueError("length must be positive")
    if value < 0 or value >= 2**length:
        raise ValueError("value does not fit in the requested length")
    return tuple((value >> shift) & 1 for shift in range(length - 1, -1, -1))

