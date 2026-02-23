# Reimplementation Plan: {Paper Title}

**Paper:** `papers/{topic}/{author-year}/`
**Implementation:** `implementations/{paper-name}/`
**Date:** {YYYY-MM-DD}

---

## Algorithm Specification

{Precise description of the algorithm to implement, referencing specific equations and pseudocode from the paper.}

### Core Equations

- Eq. {N}: {equation description}
- Eq. {M}: {equation description}

### Pseudocode

```
{Pseudocode from paper or derived from paper description}
```

## API Design

```python
# Core interface
class {ModelName}:
    def __init__(self, config: {ConfigName}) -> None: ...
    def forward(self, x: Tensor) -> Tensor: ...

# Configuration
@dataclass(frozen=True)
class {ConfigName}:
    {param1}: {type}  # {description, paper reference}
    {param2}: {type}  # {description, paper reference}
```

## Test Plan

| Test | Description | Expected |
|------|-------------|----------|
| `test_{component}_output_shape` | Verify output dimensions | {shape} |
| `test_{component}_known_input` | Known input/output pair | {expected} |
| `test_{component}_gradient_flow` | Gradients propagate | Non-zero grads |
| `test_end_to_end_overfit` | Overfit on small batch | Loss → ~0 |

## Implementation Phases

### Phase 1: Core Components
- [ ] {Component 1} — {description}
- [ ] {Component 2} — {description}

### Phase 2: Training Loop
- [ ] Data loading and preprocessing
- [ ] Training step with loss computation
- [ ] Validation loop

### Phase 3: Evaluation
- [ ] {Metric 1} computation
- [ ] Comparison with paper's reported results

## Deviations from Paper

| Aspect | Paper | Implementation | Reason |
|--------|-------|---------------|--------|
| {aspect} | {paper's choice} | {our choice} | {why} |

## Compute Requirements

- **Training:** {estimated GPU hours, hardware}
- **Inference:** {estimated time per sample}
- **Memory:** {estimated peak GPU/CPU memory}
