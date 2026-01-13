## Design Decisions

### CRC
- Implemented using polynomial division over GF(2)
- XOR operations replace subtraction
- Generator polynomial length is inferred dynamically

### Hamming (7,4)
- Syndrome calculation used for error localization
- Single-bit error correction supported
- Multi-bit errors are intentionally not corrected

### General
- Focus on clarity and educational value
- Modular separation between algorithms
