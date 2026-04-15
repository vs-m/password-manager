# manager/crypto.py
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

  # ---------- Derivar chave a partir da senha mestra ----------
def derive_key(master_password: str, salt: bytes) -> bytes:
      """Deriva uma chave de 32 bytes (AES‑256) usando Scrypt."""
      kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
      return kdf.derive(master_password.encode())

  # ---------- Criptografar ----------
def encrypt(plaintext: str, key: bytes) -> bytes:
      """Retorna nonce || ciphertext || tag."""
      aesgcm = AESGCM(key)
      nonce = os.urandom(12)               # 96 bits, recomendado para GCM
      ct = aesgcm.encrypt(nonce, plaintext.encode(), None)
      return nonce + ct                     # armazenamos tudo junto

  # ---------- Decriptografar ----------
def decrypt(ciphertext: bytes, key: bytes) -> str:
      """Recebe nonce || ciphertext || tag e devolve o texto plano."""
      nonce = ciphertext[:12]
      ct = ciphertext[12:]
      aesgcm = AESGCM(key)
      pt = aesgcm.decrypt(nonce, ct, None)
      return pt.decode()
