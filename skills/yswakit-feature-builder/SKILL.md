---
name: yswakit-feature-builder
description: Grow the yswakit personal Python toolkit from feature descriptions by adding reusable class-based modules and colocated usage guides. Use for new toolkit features or focused extensions in this repository; do not use for unrelated Python applications.
---

# YSWAKit Feature Builder

Turn the user's feature description into a small, reusable part of the `yswakit` package.

## Repository contract

- Put implementation in `src/yswakit/<feature_name>/<module_name>.py`.
- Use valid `snake_case` Python package and module names derived from the user's wording.
- Add `__init__.py` files and expose the intended public API from the feature package. Update `src/yswakit/__init__.py` only when a package-level import materially improves usability.
- Put the quick reference in `src/yswakit/<feature_name>/<usage_name>.md`. Default `usage_name` to `usage` unless the user requests another name.
- Keep tests outside the package under `tests/<feature_name>/`, following existing repository conventions when present.

## Implementation requirements

- Design a cohesive class-based public API. Split unrelated responsibilities instead of creating a catch-all utility class.
- Make public methods independently reusable from other codebases: accept ordinary Python values or documented protocols, return useful values, and avoid coupling to CLI state, repository paths, or global mutable state.
- Keep imports free of execution, network access, filesystem mutations, and configuration loading. Put such behavior behind explicit methods.
- Inject external clients, clocks, paths, or other environment-specific collaborators when that makes behavior easier to reuse and test.
- Add type hints and concise docstrings to public classes and methods. Validate inputs at the API boundary and raise specific, documented exceptions.
- Prefer the standard library. Add a runtime dependency to `pyproject.toml` only when it provides clear value for the requested feature.
- Preserve backward compatibility when extending an existing feature unless the user explicitly requests a breaking change.

## Workflow

1. Inspect `pyproject.toml`, the current package tree, and related implementations before choosing names or dependencies.
2. Implement the smallest complete API that satisfies the feature description.
3. Add focused tests for public behavior, important edge cases, and failures. Use the repository's existing test tooling; if none exists, prefer tests that introduce the least new project machinery.
4. Write or update the colocated usage guide so it matches the implemented API exactly.
5. Run the relevant tests and any configured formatter, linter, or type checker. Do not claim checks that were not run.

## Usage guide contract

The Markdown guide must be skimmable and include:

- what the feature does;
- the supported public imports;
- a minimal copy-paste example;
- constructor and public method reference, including inputs and return values;
- expected errors or important edge cases;
- dependency or environment requirements, when applicable.

Use examples that import the installed package (`from yswakit...`), not repository-relative file imports.

## Response contract

After implementation, give the user a compact quick-reference guide in the response as well as saving it in the feature's Markdown file. Include the public import, the smallest useful example, created or changed paths, and verification results. Keep the response reference synchronized with the saved guide.
