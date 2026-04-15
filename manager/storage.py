# manager/storage.py
import json
import os
from pathlib import Path
from .crypto import derive_key, encrypt, decrypt

DATA_FILE = Path.home() / ".pw_manager" / "vault.json"
SALT_FILE = Path.home() / ".pw_manager" / "salt.bin"

def _ensure_paths():
      DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
      if not SALT_FILE.exists():
          SALT_FILE.write_bytes(os.urandom(16))

def _load_salt() -> bytes:
      _ensure_paths()
      return SALT_FILE.read_bytes()

def _load_vault(key: bytes) -> dict:
      if not DATA_FILE.exists():
          return {}
      raw = DATA_FILE.read_bytes()
      try:
          decrypted = decrypt(raw, key)
          return json.loads(decrypted)
      except Exception:
          # Se a senha mestra estiver errada, o decript falha
          raise ValueError("Senha mestra incorreta")

def _save_vault(vault: dict, key: bytes):
      serialized = json.dumps(vault).encode()
      encrypted = encrypt(serialized.decode(), key)
      DATA_FILE.write_bytes(encrypted)

  # ---------- API pública ----------
def open_vault(master_password: str) -> dict:
      """Carrega o cofre (ou cria vazio) usando a senha mestra."""
      salt = _load_salt()
      key = derive_key(master_password, salt)
      try:
          return _load_vault(key)
      except ValueError:
          raise

def add_entry(vault: dict, site: str, username: str, password: str) -> dict:
      vault[site] = {"username": username, "password": password}
      return vault

def remove_entry(vault: dict, site: str) -> dict:
      vault.pop(site, None)
      return vault

def get_entry(vault: dict, site: str):
      return vault.get(site)

def persist(vault: dict, master_password: str):
      salt = _load_salt()
      key = derive_key(master_password, salt)
      _save_vault(vault, key)
