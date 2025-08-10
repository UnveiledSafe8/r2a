# r2a Documentation

## Data Structure Overview

A critical early design decision for r2a was selecting an efficient and maintainable data structure to represent instruction metadata. Several candidate structures were explored, each with distinct trade-offs in terms of time complexity, memory usage, and extensibility. After thorough evaluation, one approach emerged as the best fit for the project’s goals.

### Flat Mapping
The simplest and most straightforward approach involves a flat dictionary mapping tuples of instruction parameters directly to their metadata. This method offers O(1) worst-case lookup time, assuming fixed-size tuples and ideal hashing.

However, this approach suffers from significant drawbacks in practice:
- Maintainability issues: Interpreting tuples with varying or optional fields quickly becomes confusing, complicating the decoding logic.
- Extensibility challenges: Adding new parameters or instruction variants often requires changes to all existing tuples, which does not scale well with large or evolving instruction sets.
- Redundancy and verbosity: The need to include unused parameters as null values leads to increased memory consumption and less readable data.

While performant in theory, flat mapping’s inflexibility and maintenance burden limit its practical utility in a complex disassembler.

### Bit-by-Bit Decision Tree
This approach constructs a binary decision tree where each node corresponds to a single bit in the instruction word, branching on 0 or 1 until reaching leaf nodes representing specific instructions.
- Time complexity: Lookup requires traversing up to 32 levels (one per bit), resulting in O(32) time.
- Memory overhead: Storing nodes for every bit and path can lead to significant memory usage.
- Inefficiency for RISC-V: Because many bits are “don’t care” or unused for instruction identification, this method wastes resources traversing irrelevant bits.

Although highly structured and predictable, this method is overly granular and inefficient for RISC-V’s relatively compact opcode and function field encoding.

### Bit Masking Mapping
A middle ground is to use a dictionary keyed by opcode, where each opcode maps to a list or tuple of candidate instructions, differentiated by further fields such as funct3, funct5, and funct7.
- Time complexity: Lookup within a single opcode bucket is O(n), where n is the number of instructions sharing that opcode.
- Practical performance: Since most opcodes correspond to fewer than 32 instructions, the average lookup cost is typically less than the full 32-bit decision tree traversal.
- Memory usage: More compact than bit-by-bit trees, but still redundant when multiple instructions share many common fields.
- Structural limitations: Lacks explicit hierarchy of decision parameters, complicating maintenance and extension when new parameters or instruction variants are introduced.

This approach balances memory and performance but does not fully leverage the structured nature of RISC-V instruction encoding.

### Parameter Decision Tree (Chosen Structure)
The final and preferred design implemented in r2a is a nested decision tree keyed by instruction parameters, where each level specifies:
- The parameter name (e.g., "opcode", "funct3", "funct5", "funct7"),
- A dictionary mapping possible values for that parameter to either:
  - A further nested parameter dictionary, or
  - A leaf node containing the instruction metadata.

This approach provides several key advantages:
- Scalability: New parameters or instruction variants can be added without modifying existing branches.
- Maintainability: The metadata explicitly defines the next parameter to inspect at each node, improving code readability and debugging.
- Time complexity: Lookup takes O(k) time, where k is the number of parameters needed to uniquely identify the instruction (rarely exceeding 3 for RISC-V).
- Memory efficiency: Comparable to flat mapping with minimal overhead for storing parameter keys, avoiding redundant tuples with unused fields.

Overall, the parameter decision tree combines the clarity and extensibility of hierarchical structures with near-constant-time lookup efficiency, making it an ideal balance for RISC-V disassembly.