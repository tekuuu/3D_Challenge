# Contributing to Project Chimera

Thank you for contributing! This guide lists initial steps for new contributors.

1. Setup
   - Install Python 3.12 and create a virtualenv
   - Install dev deps: `pip install -r requirements.txt`
   - Run `make setup` to prepare environment

2. Workflow
   - Create a topic branch from `main`.
   - Open a PR with clear description and link to related spec requirement in `specs/`.
   - Ensure tests and `ruff` pass locally.

3. PR checklist
   - Code references a spec in `specs/` or an ADR.
   - Add/update tests for behavior changes.
   - Update `docs/` if the public contract changed.
