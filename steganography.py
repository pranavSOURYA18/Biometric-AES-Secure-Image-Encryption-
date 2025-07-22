
import numpy as np

def lsb_embed(cover_image, secret_data):
    flat_cover = cover_image.flatten()
    data_length = len(secret_data).to_bytes(4, 'big')
    full_data = data_length + secret_data
    if len(full_data) * 8 > len(flat_cover):
        raise ValueError("Cover image is too small to embed the data.")
    for i in range(len(full_data) * 8):
        byte_index = i // 8
        bit_index = 7 - (i % 8)
        bit = (full_data[byte_index] >> bit_index) & 1
        flat_cover[i] = (flat_cover[i] & ~1) | bit
    return flat_cover.reshape(cover_image.shape)

def lsb_extract(stego_image):
    flat = stego_image.flatten()
    bits = [flat[i] & 1 for i in range(32)]  # first 32 bits = 4 bytes of length
    length = int(''.join(str(b) for b in bits), 2)
    bits = [flat[i] & 1 for i in range(32, 32 + length * 8)]
    bytes_out = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        bytes_out.append(byte)
    return bytes(bytes_out)
