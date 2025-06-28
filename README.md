# 🔐 Cryptography Toolkit

A modern, user-friendly desktop application built using **Tkinter** and **CustomTkinter**, offering encryption, decryption, key generation, and digital signature tools for a wide range of classical and modern cryptographic algorithms.

---

## 📦 Features

- **Modern GUI Interface**
  - Dark/light theme toggle
  - Custom title and status bars
  - Tabbed navigation for better UX

- **Supported Classical Ciphers**
  - Caesar Cipher
  - Playfair Cipher
  - Hill Cipher (2x2)
  - Vigenère Cipher
  - Rail Fence Cipher

- **Symmetric Encryption**
  - DES (simplified XOR version for demo purposes)

- **Asymmetric Encryption**
  - RSA (Key generation, encryption, decryption)

- **Digital Signature**
  - DSA (Key generation, signing, verification)

- **Extras**
  - Key matrix and hex output displays
  - Input validation and copy-to-clipboard functionality
  - Status messages and tooltips for user guidance

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Required Libraries:
  - `customtkinter`
  - `tkinter` (preinstalled in Python)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cryptography-toolkit.git
cd cryptography-toolkit

# Install dependencies
pip install customtkinter

# Run the application
python combined.py
