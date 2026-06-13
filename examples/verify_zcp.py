"""Construct and verify the legacy length-36 ZCP."""

from sequence_design import kronecker_zcp, zero_correlation_zone


first_kernel = (
    -1, -1, -1, -1, 1, -1, -1, 1, -1,
    -1, 1, -1, -1, -1, 1, 1, 1, 1,
)
second_kernel = (
    -1, 1, 1, 1, -1, -1, -1, 1, -1,
    1, -1, 1, 1, -1, 1, 1, 1, -1,
)

first, second = kronecker_zcp(first_kernel, second_kernel)
print(f"length={len(first)}, zone={zero_correlation_zone(first, second)}")

