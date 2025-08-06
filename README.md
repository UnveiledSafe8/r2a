# R2A

---

## Features

- Support for core RISC-V instruction set [technical specifications][https://lf-riscv.atlassian.net/wiki/spaces/HOME/pages/16154769/RISC-V+Technical+Specifications]:
    - **RV32I-2.1**
    - **RV64I-2.1**
    - **Extensions: A-2.1, M-2.0**
- Accurate label generation
- Parse raw binary (.bin) files in little-endian
- No external dependencies apart from python
- Built for extension: ideal foundation for simulators or assemblers

## Limitations

- ELF files not supported
- No validation or instruction legality checks
- No pseduoinstructions

## Roadmap

- More instruction sets
- ELF file parsing
- Legality checks
- Library + GUI application

## Design Decisions

- Instruction mnemonics are organized in separate hardcoded tables by type and extension, enabling fast in-memory lookups, modular maintenance, and easy extension without external dependencies.

## Contributions

- Anthony Schurle (Author)