# WI-1 Anonymity Fix Report

Date: 2026-07-24

Scope:
- Remove reviewer-cited identity and affiliation leaks from the repository content.
- Do not address git history in this pass, per user instruction.

Files updated:
- `spectra/__init__.py`
- `setup.py`
- `pyproject.toml`
- `LICENSE`

Changes made:
- Removed the named author field from `spectra/__init__.py`.
- Replaced `setup.py` author metadata with `Anonymous`.
- Replaced `pyproject.toml` project author metadata with `Anonymous`.
- Replaced the license copyright holder with `Anonymous`.

Verification:
- Searched the repository content for `Neryva Lab`, `Luke Green`, and `__author__`.
- The reviewer-cited identity strings are no longer present in `spectra/__init__.py`, `setup.py`, `pyproject.toml`, or `LICENSE`.
- The only remaining `__author__` hit in the repo is `experiments/bpgs_analysis/analysis/__init__.py`, which uses the generic label `BPGS Authors` and is not the cited leak.

Notes:
- Git history was intentionally not addressed in this pass.
- This completes WI-1 as a repository-content anonymity cleanup.
