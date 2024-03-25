from cryptography.fernet import Fernet, InvalidToken
from tinydb import TinyDB, Query
import vault

def insert(vault_path: str, vault_password: str, name: str, username: str, password: str, description: str):
    doc = {
        'type': 'registered',
        'name': name,
        'username': username,
        'password': password,
        'description': description
    }
    descrypt_res = vault.decrypt(vault_path, vault_password)
    if not descrypt_res:
        return False
    db = TinyDB(vault_path)
    db.insert(doc)
    db.close()
    vault.encrypt(vault_path, vault_password)
    return True

def get(vault_path: str, vault_password: str):
    decrypt_res = vault.decrypt(vault_path, vault_password)
    if not decrypt_res:
        return False
    db = TinyDB(vault_path)
    query = Query()
    result = db.search(query.type == 'registered')
    db.close()
    vault.encrypt(vault_path, vault_password)
    return result