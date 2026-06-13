"""Binary complementary-sequence design and validation tools."""

from .constructions import kronecker_zcp
from .correlation import (
    aperiodic_autocorrelation,
    aperiodic_cross_correlation,
    to_bipolar,
)
from .properties import (
    is_gcs,
    is_optimal_czcs,
    is_zcp,
    zero_correlation_zone,
)
from .sequences import transition_positions, transition_sequence

__all__ = [
    "aperiodic_autocorrelation",
    "aperiodic_cross_correlation",
    "is_gcs",
    "is_optimal_czcs",
    "is_zcp",
    "kronecker_zcp",
    "to_bipolar",
    "transition_positions",
    "transition_sequence",
    "zero_correlation_zone",
]

__version__ = "1.0.0"

