<!--
Sync Impact Report:
- Version: 1.0.0 → 1.1.0
- Change Type: MINOR version (new principles added)
- Modified Principles: None
- Added Sections:
  - Principle VI: Build Script Standards (logging and error handling)
  - Principle VII: Linux Text File Standards (line endings and file termination)
- Removed Sections: None
- Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section already complete
  ✅ spec-template.md - No changes needed
  ✅ tasks-template.md - No changes needed
- Follow-up TODOs: None
-->

# gem5_riscv_rt Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All work starts from specifications. Feature/requirement/architecture changes MUST be reflected in spec documents before implementation. Implementation commits MUST reference the spec item being satisfied.

**Rationale**: Ensures traceability from requirements to implementation to verification, preventing scope creep and enabling reproducible research.

### II. Unambiguous Specifications

Specifications MUST be unambiguous, testable, and traceable:
- **Unambiguous**: Avoid vague expressions (e.g., "fast", "moderate", "as much as possible"). Use concrete numbers and conditions.
- **Testable**: Each requirement MUST be verifiable through testing, measurement, or simulation.
- **Traceable**: Requirement IDs ↔ implementation code/scripts ↔ experimental results (reports) MUST be linkable.

**Rationale**: Enables objective verification and reproducibility of simulation experiments, critical for design-space exploration.

### III. Design First, Optimization Later

Initial development prioritizes correctness and reproducibility over performance. Performance optimization is addressed only after baseline stabilization and MUST be managed through separate "Optimization specs."

**Rationale**: Premature optimization introduces complexity that obscures correctness issues. Stable baselines enable meaningful performance comparisons.

### IV. Atomic Commits

Git commits MUST be atomic, containing one logical change. Follow Linux/gem5 commit style:
- **Summary**: ~50 characters, imperative mood
- **Body**: 72-character wrapping, explains what and why (not how)
- **Reference**: Link to spec item or issue when applicable

**Rationale**: Atomic commits enable clean history, easy bisection, and clear code review.

### V. Source-Build Separation

Source code and build artifacts MUST be strictly separated:
- **Source**: `src/`, `configs/`, `workloads/`, `docs/`, `.specify/`
- **Build**: All build outputs under `build/` directory
- **External**: Manage via Git submodules with pinned versions

**Rationale**: Prevents build pollution of source tree, enables reproducible builds, and simplifies cleanup.

### VI. Build Script Standards

All component builds MUST use dedicated build scripts with structured logging:
- **Build Scripts**: Each component (gem5, Zephyr, NVMain) MUST have a dedicated build script in `scripts/`
- **Logging**: Build output MUST be logged to files (e.g., `build/gem5/build.log`)
- **Error Handling**: Only errors MUST be printed to stdout; full logs remain in log files
- **Exit Codes**: Build scripts MUST return non-zero exit codes on failure

**Rationale**: Structured logging enables debugging without cluttering terminal output. Log files provide complete build history for troubleshooting.

### VII. Linux Text File Standards

All text files MUST follow Linux conventions:
- **Line Endings**: Use LF (Line Feed, `\n`) only, not CRLF (Windows-style)
- **File Termination**: All text files MUST end with a newline character
- **Encoding**: Use UTF-8 encoding without BOM

**Rationale**: Ensures compatibility with Linux development tools, prevents git diff noise from line ending changes, and follows POSIX standards.

## Development Workflow

### Unit of Work

For each new feature or change:
1. Update relevant requirement/spec documents
2. Implement code/scripts/configuration
3. Execute minimum test/simulation
4. Summarize results and commit

### Branching & Review

- `main` branch MUST always be buildable and pass basic simulations
- Use feature branches for functionality/experiments
- Merge to main only after review (self-review with checklist is acceptable)
- Review checklist MUST verify spec alignment and test coverage

### Commit Standards

Follow open-source conventions (Linux/gem5 style):
- Commits are atomic (one logical change)
- Summary line: 50 characters, imperative mood
- Body: 72-character wrapping, explains context and rationale
- Reference spec IDs or issue numbers

## Repository & Build Layout

### Top-Level Structure

```
gem5_riscv_rt/
├── src/                  # Source code (read-only during builds)
│   ├── gem5/            # gem5 submodule
│   ├── zephyr/          # Zephyr RTOS submodule
│   └── nvmain/          # (Optional) NVMain submodule
├── configs/             # gem5 RISC-V full-system configs
├── workloads/           # Automotive workload definitions
├── scripts/             # Build/run/analysis automation
├── docs/                # Specs, experiment plans, DSE reports
├── build/               # All build outputs
│   ├── gem5/
│   ├── zephyr/
│   └── nvmain/
└── .specify/            # Specification framework
```

### Build Rules

- All builds execute in `build/` subdirectories
- Source directories (`src/`) treated as read-only
- Build/execution scripts in `scripts/` for reproducibility
- Submodule versions (tag/commit) MUST be documented in CHANGELOG and specs

## External Code & Licensing

### External Components

- gem5, Zephyr RTOS, NVMain, benchmarks: Respect each project's license
- Submodules MUST specify version (tag/commit)
- Version changes MUST be recorded in CHANGELOG and specs

### License Compliance

- Prevent license violations when mixing closed-source code with copyleft licenses (e.g., GPL)
- Maintain SBOM and license information in `docs/license/`
- Use automated scripts for license tracking

## Quality & Testing

### Minimum Quality Standards

- All major simulation configurations MUST execute successfully with example inputs
- "Basic scenarios" defined in specs MUST have automated execution scripts

### Test Types

- **Smoke Test**: Verify build and full simulation complete successfully at least once
- **Regression Test**: Core configurations maintain statistics (IPC, miss rate, etc.) within tolerance
- **Consistency Check**: Verify config/scripts match documentation for same spec ID

## Documentation

### Documentation Requirements

All major decisions (architecture choices, cache/memory configurations, workload selection criteria) MUST be documented.

### Documentation Structure

Follow this format:
1. Problem definition
2. Assumptions
3. Alternatives considered
4. Selected option
5. Rationale
6. TODO items

### Traceability

Specs, design documents, and experimental results MUST be cross-linked to maintain traceability.

## Governance

This constitution supersedes all other development practices. Amendments require:
1. Documentation of proposed changes
2. Review and approval
3. Migration plan for affected code/specs

All pull requests and code reviews MUST verify compliance with this constitution. Complexity that violates principles MUST be justified in writing.

**Version**: 1.1.0 | **Ratified**: 2025-11-23 | **Last Amended**: 2025-11-23
