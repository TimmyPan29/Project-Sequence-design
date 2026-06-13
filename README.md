# Binary Complementary Sequence Design

A reproducible signal-processing project for constructing, searching, and
validating binary zero-correlation pairs (ZCPs), Golay complementary sets
(GCSs), and cross Z-complementary sets (CZCSs).

The project began as MATLAB code accelerated by Windows MEX modules. This
repository preserves that research history while providing a tested,
cross-platform Python implementation of the core mathematics.

## Highlights

- Reproduces reported ZCPs with parameters $(34,18)$, $(36,26)$, and $(41,21)$.
- Implements binary sequence generation from transition positions.
- Provides a single tested definition of positive-lag AACF and ACCF.
- Includes reference exhaustive searches for small sequence lengths.
- Validates all 1,581 archived CZCS records and reports historical data issues.
- Structurally audits 6,798 archived GCS index records.
- Uses only the Python standard library at runtime.

## Validation Summary

| Artifact | Result |
|---|---:|
| Kronecker ZCP $(34,18)$ | Pass |
| Kronecker ZCP $(36,26)$ | Pass |
| Exhaustive-search ZCP $(41,21)$ | Pass |
| CZCS records at $L=2,\ldots,8$ | 1,050 / 1,050 valid |
| CZCS records at $L=9$ | 0 / 294 valid |
| CZCS records at $L=10$ | 0 / 233 valid |
| CZCS records at $L=11$ | 4 / 4 valid |

The $L=9$ and $L=10$ files are preserved unchanged. Their failure is a
reproducible historical-data finding, documented in
[docs/VALIDATION_REPORT.md](docs/VALIDATION_REPORT.md).

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
sequence-design validate
```

Compute an AACF:

```bash
sequence-design acf "++-"
# 3 0 -1
```

Measure the zero-correlation-zone width of a pair:

```bash
sequence-design zcp "++" "+-"
# 2
```

## Mathematical Convention

Binary inputs in $\{0,1\}$ are mapped to the bipolar alphabet
$\{-1,+1\}$. For equal-length sequences $\mathbf{x}$ and $\mathbf{y}$,
the positive-lag aperiodic cross-correlation is

$$
R_{\mathbf{x},\mathbf{y}}(u)
=
\sum_{n=0}^{L-u-1}x_{n+u}y_n,
\qquad 0\leq u<L.
$$

A pair is an $(L,Z)$ ZCP when

$$
R_{\mathbf{x}}(u)+R_{\mathbf{y}}(u)=0,
\qquad 1\leq u<Z.
$$

The optimal CZCS validator reproduces the archived final-project criterion:
four sequences must form a full complementary set and their cyclic adjacent
ACCF sum must be zero at every nonnegative lag.

## Repository Layout

```text
src/sequence_design/   Portable correlation, construction, search, and CLI code
tests/                 Unit, regression, and command-line tests
data/reference/        Archived GCS/CZCS result tables
examples/              Small reproducible demonstrations
docs/                  Architecture, validation, and CV notes
legacy/                Original MATLAB, C, and Windows MEX artifacts
reports/               Original project presentations
archives/              Original submitted RAR packages
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the module boundaries.

## Historical Implementation

The original implementation used MATLAB scripts and `.mexw64` binaries.
Those binaries are Windows-only and cannot be loaded on macOS or Linux.
Several scripts also contain hard-coded Windows output paths and stale
function names. They are retained under `legacy/` for provenance, while all
new verification runs through the portable implementation.

## Testing

```bash
make test
make validate
```

Tests cover correlation orientation, binary/bipolar equivalence, transition
generation, known ZCP constructions, small exhaustive searches, CLI behavior,
and every archived CZCS row.

## License

Code in the portable implementation is released under the MIT License.
Historical reports and submitted artifacts remain included for academic
provenance.
