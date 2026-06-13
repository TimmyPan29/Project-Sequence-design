"""Algebraic constructions retained from the MATLAB project."""

from collections.abc import Sequence

from .correlation import to_bipolar


def _kronecker(first: Sequence[int], second: Sequence[int]) -> tuple[int, ...]:
    return tuple(left * right for left in first for right in second)


def kronecker_zcp(
    first_kernel: Sequence[int],
    second_kernel: Sequence[int],
    *,
    golay_first: Sequence[int] = (1, 1),
    golay_second: Sequence[int] = (1, -1),
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Apply the construction used by the legacy length-34/36 scripts."""
    c = to_bipolar(first_kernel)
    d = to_bipolar(second_kernel)
    a = to_bipolar(golay_first)
    b = to_bipolar(golay_second)
    if len(c) != len(d) or len(a) != len(b):
        raise ValueError("each input pair must have equal lengths")

    reverse_a = tuple(reversed(a))
    reverse_b = tuple(reversed(b))
    t1 = tuple((left + right) // 2 for left, right in zip(a, b, strict=True))
    t2 = tuple((left - right) // 2 for left, right in zip(a, b, strict=True))
    t3 = tuple(
        (left - right) // 2
        for left, right in zip(reverse_a, reverse_b, strict=True)
    )
    t4 = tuple(
        (left + right) // 2
        for left, right in zip(reverse_a, reverse_b, strict=True)
    )

    first = tuple(
        left + right
        for left, right in zip(_kronecker(c, t1), _kronecker(d, t2), strict=True)
    )
    second = tuple(
        left - right
        for left, right in zip(_kronecker(c, t3), _kronecker(d, t4), strict=True)
    )
    return first, second

