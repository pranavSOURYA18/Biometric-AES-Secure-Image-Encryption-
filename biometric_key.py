import face_recognition
import hashlib
import numpy as np

def generate_key_from_face(image_np):
    encodings = face_recognition.face_encodings(image_np)
    if len(encodings) == 0:
        raise ValueError("No face detected")
    face_vec = encodings[0]
    return hashlib.sha256(face_vec.tobytes()).digest()[:32]
