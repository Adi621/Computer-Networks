def encode_hamming74(nibble: list[int]) -> list[int]:
    """
    Encode 4-bit data using Hamming(7,4).
    """
    d1, d2, d3, d4 = nibble

    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p4 = d2 ^ d3 ^ d4

    return [p1, p2, d1, p4, d2, d3, d4]


def decode_hamming74(encoded: list[int]) -> list[int]:
    """
    Decode and correct a single-bit error in Hamming(7,4).
    """
    p1, p2, d1, p4, d2, d3, d4 = encoded

    s1 = p1 ^ d1 ^ d2 ^ d4
    s2 = p2 ^ d1 ^ d3 ^ d4
    s4 = p4 ^ d2 ^ d3 ^ d4

    error_position = s1 + (s2 << 1) + (s4 << 2)

    if 1 <= error_position <= 7:
        encoded[error_position - 1] ^= 1

    return [encoded[2], encoded[4], encoded[5], encoded[6]]
