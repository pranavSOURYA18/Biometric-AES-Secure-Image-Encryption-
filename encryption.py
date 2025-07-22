
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import numpy as np

def encrypt_image(img_np, key, mode):
    data = img_np.tobytes()
    iv = get_random_bytes(16)
    if mode == "CBC":
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return ciphertext, iv
    elif mode == "CFB":
        cipher = AES.new(key, AES.MODE_CFB, iv)
        ciphertext = cipher.encrypt(data)
        return ciphertext, iv
    elif mode == "GCM":
        cipher = AES.new(key, AES.MODE_GCM, iv)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return ciphertext, iv, tag
    else:
        raise ValueError("Unsupported AES mode")

def decrypt_image(ciphertext, iv, key, mode, tag=None):
    if mode == "CBC":
        cipher = AES.new(key, AES.MODE_CBC, iv)
        data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    elif mode == "CFB":
        cipher = AES.new(key, AES.MODE_CFB, iv)
        data = cipher.decrypt(ciphertext)
    elif mode == "GCM":
        cipher = AES.new(key, AES.MODE_GCM, iv)
        data = cipher.decrypt_and_verify(ciphertext, tag)
    else:
        raise ValueError("Unsupported AES mode")
    return np.frombuffer(data, dtype=np.uint8)
