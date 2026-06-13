# Architecture

## Design Goal

The refactor separates mathematical definitions, search policy, historical
artifacts, and presentation. Correlation behavior therefore has one source of
truth and can be tested without MATLAB or a platform-specific MEX binary.

## Modules

### `correlation.py`

Defines alphabet normalization and positive-lag AACF/ACCF. Every property,
search, construction, and validator imports these functions.

### `sequences.py`

Provides deterministic sequence representations:

- transition positions to binary sequences;
- binary sequences to transition positions;
- fixed-width integer enumeration.

### `properties.py`

Implements ZCP, GCS, and optimal-CZCS predicates. It contains no file access or
search loops, which keeps definitions independently testable.

### `constructions.py`

Implements the Kronecker construction used by the historical length-$34$ and
length-$36$ MATLAB scripts.

### `search.py`

Contains transparent reference searches. These routines prioritize
reproducibility over large-scale performance and are intended for small
lengths, tests, and algorithm demonstrations.

### `validation.py`

Loads archived datasets and evaluates them through the same property functions
used by the search code. It also contains exact fixtures recovered from the
original reports.

### `cli.py`

Exposes AACF calculation, ZCP measurement, and full repository validation.

## Data Flow

```text
input sequence
    |
    v
alphabet normalization
    |
    v
AACF / ACCF primitives
    |
    +----> ZCP / GCS / CZCS predicates
    |              |
    |              +----> search
    |              |
    |              +----> archived-data validation
    |
    +----> Kronecker construction verification
```

## Complexity

Correlation is evaluated directly in $O(L^2)$ time and $O(L)$ output space.
The exhaustive GCS reference search evaluates
$\binom{2^L+N-1}{N}$ multisets for set size $N$, so it is deliberately limited
to small $L$. Large searches should retain the transition-position pruning
strategy or add parallel/native acceleration behind the tested API.

