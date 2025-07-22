from PIL import Image
import numpy as np

def visualize_cipher(ciphertext, shape):
    try:
        reshaped = np.frombuffer(ciphertext, dtype=np.uint8).reshape(shape)
    except:
        reshaped = np.frombuffer(ciphertext[:np.prod(shape)], dtype=np.uint8).reshape(shape)
    return Image.fromarray(reshaped)
