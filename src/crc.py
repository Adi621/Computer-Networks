def compute_crc(data: int, generator: int) -> int:
    """
    Compute CRC remainder using polynomial division over GF(2).
    """
    gen_len = generator.bit_length()
    remainder = data << (gen_len - 1)

    while remainder.bit_length() >= gen_len:
        shift = remainder.bit_length() - gen_len
        remainder ^= generator << shift

    return remainder


def verify_crc(data: int, generator: int, crc: int) -> bool:
    """
    Verify received CRC.
    """
    return compute_crc(data, generator) == crc
