def encode_block(data_bits: list[int], redundancy: int) -> list[int]:
    """
    Encode data bits by adding simple redundancy.

    Args:
        data_bits: original data bits
        redundancy: number of redundant repetitions

    Returns:
        Encoded bit sequence
    """
    encoded = []
    for bit in data_bits:
        encoded.extend([bit] * redundancy)
    return encoded


def decode_block(encoded_bits: list[int], redundancy: int) -> list[int]:
    """
    Decode redundant block code using majority voting.

    Args:
        encoded_bits: received encoded bits
        redundancy: redundancy factor used in encoding

    Returns:
        Decoded data bits
    """
    decoded = []
    for i in range(0, len(encoded_bits), redundancy):
        block = encoded_bits[i:i + redundancy]
        decoded.append(1 if sum(block) > redundancy / 2 else 0)
    return decoded
