from cryptography.fernet import Fernet, InvalidToken
from tinydb import TinyDB, Query
import random
import string
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

def get_pass_length_range():
    lengths = []
    counter = 0
    for i in range(0,100):
        counter += 1
        lengths.append(counter)
    return lengths

def generate_password(length: int, uppercase: bool, numbers: bool, special_chars: bool):
    chars = string.ascii_lowercase
    if uppercase:
        chars += string.ascii_uppercase
    if numbers:
        chars += string.digits
    if special_chars:
        chars += string.punctuation
    chars = ''.join(random.sample(chars, len(chars)))
    password = ''.join(random.choice(chars) for i in range(length))
    return password