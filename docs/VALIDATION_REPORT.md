# Validation Report

## Scope

The validation covers:

1. C and MATLAB algorithm semantics visible in the historical source;
2. three exact ZCP results recoverable from scripts and reports;
3. every archived `length_*_CZCS.csv` row;
4. command-line and small exhaustive-search behavior.

## Correlation Definition

The C function `aacfse2_c.c` counts equal binary symbols at each lag and
computes

$$
2N_{\mathrm{equal}}(u)-(L-u).
$$

After mapping $0\mapsto-1$ and $1\mapsto+1$, this is exactly

$$
R_{\mathbf{x}}(u)
=
\sum_{n=0}^{L-u-1}x_{n+u}x_n.
$$

The archived CZCS tables establish the ACCF direction as

$$
R_{\mathbf{x},\mathbf{y}}(u)
=
\sum_{n=0}^{L-u-1}x_{n+u}y_n.
$$

Reversing $\mathbf{x}$ and $\mathbf{y}$ rejects valid archived rows at several
lengths, confirming that the orientation is behaviorally significant.

## ZCP Regression Results

| Source | Expected $Z$ | Measured $Z$ |
|---|---:|---:|
| `kronecker_L34_Z18.m` | 18 | 18 |
| `kronecker_L36_Z26.m` | 26 | 26 |
| `L41_result.txt` | 21 | 21 |

The legacy Kronecker scripts construct valid pairs, but their subsequent
MATLAB `xcorr` slicing begins at index $364$. For sequence lengths $34$ and
$36$, that slice is empty. The portable implementation validates the complete
positive-lag AACF instead.

## Archived CZCS Results

| Length | Rows | Valid | Invalid |
|---:|---:|---:|---:|
| 2 | 40 | 40 | 0 |
| 3 | 176 | 176 | 0 |
| 4 | 128 | 128 | 0 |
| 5 | 448 | 448 | 0 |
| 6 | 224 | 224 | 0 |
| 7 | 10 | 10 | 0 |
| 8 | 24 | 24 | 0 |
| 9 | 294 | 0 | 294 |
| 10 | 233 | 0 | 233 |
| 11 | 4 | 4 | 0 |
| **Total** | **1,581** | **1,054** | **527** |

The $L=9$ and $L=10$ records are structurally well-formed binary rows, but
each violates at least one full complementary-set or cyclic ACCF condition.
They are retained unchanged as historical inputs. The tests assert these
counts so future changes cannot silently redefine the mathematics to make the
files pass.

## Archived GCS Index Results

`length_7_GCS.csv` contains 6,798 unique, nondecreasing four-index rows with an
index range of $1$ to $64$. The archived script shown in `final_project_2.m`
enumerates $2^7=128$ binary sequences, but the file's missing candidate-index
map is required to translate these $64$ indices back to sequences.

The file therefore passes structural validation only. Treating the indices as
either one-based or zero-based direct binary enumeration does not reproduce a
GCS, so claiming mathematical validation would be unsupported.

## Legacy Execution Boundaries

- `.mexw64` binaries target 64-bit Windows.
- The current environment has no MATLAB or GNU Octave runtime.
- Final generalized MEX source code is absent from the archive.
- Legacy scripts contain hard-coded `C:/...` and `F:/...` paths.
- The length-$41$ scripts call `finding_seq31`; the available implementation
  is named `finding_seq41`.
- `final_project_2.m` calls `accf`, while the supplied binary is `accf_c`.
- The length-$37$ custom combination function intentionally allocates and
  searches only one tenth of the full combination count.

The original binaries were therefore inspected but not executed. Their
observable source behavior and archived outputs are covered by the portable
regression suite.
