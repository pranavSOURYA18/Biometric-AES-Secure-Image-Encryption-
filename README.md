🔐 Biometric-AES: Secure Image Encryption with Facial Key and Steganography

Biometric-AES is a multi-layered image encryption system that leverages facial recognition for biometric authentication, AES encryption for data security, and LSB steganography to embed encrypted images into carrier images. The system provides a secure, user-friendly Streamlit interface to manage encryption, embedding, and decryption workflows efficiently.

🚀 Features
- 🔑 Facial Recognition-Based Key Generation
  No need to remember or share manual passwords — user-specific AES keys are generated from facial features.
- 🔐 AES Encryption (CBC, CFB, GCM Modes)
  Encrypts images using strong cryptographic standards with options to select encryption modes.
- 🕵️‍♂️ LSB Steganography
  Hides encrypted data in carrier images using the Least Significant Bit method for stealthy transmission.
- 🌐 Streamlit Interface
  A clean and simple web UI for performing encryption, steganographic embedding, and decryption.

🛠️ Tech Stack
- Languages & Frameworks: Python, Streamlit
- Libraries: face_recognition, cryptography, numpy, PIL
- Techniques: AES Encryption (CBC/CFB/GCM), LSB Steganography, Biometric Key Generation

📦 Installation
1. Clone the repository:
   git clone https://github.com/pranavSOURYA18/biometric-aes-encryption.git
   cd biometric-aes-encryption

2. Install dependencies:
   pip install -r requirements.txt

3. Run the Streamlit app:
   streamlit run app.py

📂 Project Structure
├── app.py                   # Streamlit interface
├── encryption/              # AES encryption & decryption logic
├── steganography/           # LSB steganography embedding and extraction
├── biometric/               # Facial recognition & key generation
├── utils/                   # Helper functions
├── assets/                  # Sample images
└── README.md

🧠 How It Works
1. Face Recognition: Captures facial features and derives a secure biometric key.
2. AES Encryption: Encrypts selected image using the biometric key and chosen AES mode.
3. Steganography: Embeds encrypted image into a carrier image using LSB.
4. Decryption: Extracts and decrypts the hidden image if the correct biometric key is used.

🛡️ Use Cases
- Secure biometric-based data transmission
- Confidential document/image storage
- Personal encryption applications

🧑‍💻 Author
Pranav Sourya Bhavirisetty
Email: pranavsourya.bhavirisetty@gmail.com
GitHub: https://github.com/pranavSOURYA18

📃 License
This project is licensed under the MIT License.

⭐ If you found this project useful, feel free to star it and share!
