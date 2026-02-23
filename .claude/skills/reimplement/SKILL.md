---
name: reimplement
description: Reimplement a paper's core method in Python using test-driven development.
---

# /reimplement

Reimplement a paper's method in Python with TDD.

## Arguments

- `$ARGUMENTS` — Path to the paper directory (e.g., `papers/transformers/vaswani-2017/`)
- Optional flag: `--en` — Output conversation and documentation in English (default: Japanese)

## Workflow

1. **Read the Paper**:
   - Read existing `notes.md` and `claims.md` for the paper
   - If notes don't exist, suggest running `/read-paper` first
   - Identify the core algorithm, equations, and architectural choices to implement

2. **Create Implementation Plan**:
   - Generate `implementations/{paper-name}/README.md` following `docs/templates/reimplementation-plan.md`
   - Define: algorithm specification, API design, test plan, implementation phases, known deviations
   - **Present the plan to the user and wait for approval before coding**

3. **Setup**:
   - Create the implementation directory structure
   - Create `requirements.txt` with dependencies
   - Set up `venv`: `python3 -m venv .venv`

4. **TDD Implementation** (for each component):
   - Write test first (`tests/test_{component}.py`)
   - Run test — confirm it FAILS
   - Implement minimal code to pass (`src/{component}.py`)
   - Run test — confirm it PASSES
   - Refactor while keeping tests green

5. **Integration**:
   - Wire components together
   - Add end-to-end test (overfit on small batch)
   - Verify overall functionality

6. **Documentation**:
   - Document any deviations from the paper in `README.md`
   - Note compute requirements and expected results

## Important

- **Interactive process**: Ask the user for design decisions (architecture choices, hyperparameter defaults, scope)
- **Type hints** on all function signatures
- **Immutable patterns**: prefer creating new objects over mutation
- **pytest** for testing, target 80%+ coverage
- Always run tests after each implementation step
- **Language**: Default conversation/documentation in Japanese. If `--en` is in `$ARGUMENTS`, use English. Code comments and variable names are always in English.
