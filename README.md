# AlgoLang

> **Competitive Programming Compiler & Static Analyzer**  
> A domain-specific language and compiler built for competitive programmers who want more than just *"it compiled."*

---

## What Is AlgoLang?

AlgoLang is:

- A **DSL** with minimal, indentation-based syntax focused on algorithm design
- A **static analyzer** that estimates Big-O complexity, detects overflow risks, and flags expensive patterns
- A **transpiler** that converts `.algo` source files into optimized, competition-ready C++
- A **compiler driver** that invokes `g++` on the generated code to produce a final executable

---

## Quick Start

```bash
# Install in editable mode (creates the `algolang` command)
pip install -e ".[dev]"

# Parse a .algo file and dump the AST
algolang compile tests/cases/two_sum.algo --ast

# Run tests
pytest tests/ -v
```

---

## Example (`.algo` source)

```
read n
read array a[n]
sort a
for i in 0..n-1:
    for j in i+1..n-1:
        if a[i] + a[j] == 0:
            print i, j
            break
```

---

## Project Structure

```
algolang/
├── lexer/
│   ├── tokens.py          # Token type enum & Token dataclass
│   └── lexer.py           # Tokenizer (emits INDENT/DEDENT)
├── parser/
│   ├── ast_nodes.py       # All AST node dataclasses
│   └── parser.py          # Recursive descent parser
├── analyzer/
│   ├── semantic.py        # (Phase 2) Type checking, scope resolution
│   ├── complexity.py      # (Phase 3) Big-O estimator
│   ├── overflow.py        # (Phase 3) Range propagation
│   ├── patterns.py        # (Phase 3) TLE pattern recognizer
│   └── suggestions.py     # (Phase 3) Suggestion database
├── codegen/
│   └── cpp_emitter.py     # (Phase 4) AST → C++ transpiler
├── cli/
│   └── main.py            # CLI entry-point (Typer)
└── tests/
    ├── cases/             # .algo input files
    ├── expected/          # Golden output files
    └── test_pipeline.py   # End-to-end test runner
```

---

## Build Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | **Lexer & Parser** — tokenize + build AST | 🟢 Active |
| 2 | Semantic Analysis & Type Checking | ⬜ Planned |
| 3 | CP Analyzer — complexity, overflow, suggestions | ⬜ Planned |
| 4 | C++ Code Generator | ⬜ Planned |
| 5 | CLI, Output & Developer Experience | ⬜ Planned |
| 6 | Advanced Analysis & Roadmap Features | ⬜ Planned |
