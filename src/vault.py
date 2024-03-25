from cryptography.fernet import Fernet, InvalidToken
from tinydb import TinyDB, Query
import hashlib
import hashing

def create(path: str, name: str, password: str):
    db = TinyDB(f'{path}/{name}.json')
    hash = hashing.md5(password)
    db.insert({'type':'inner_auth', 'value':hash})
    db.close()
    encrypt(f'{path}/{name}.json', password)

def auth(filepath: str, password: str):
    decrypt_res = decrypt(filepath, password)
    if not decrypt_res:
        return False
    db = TinyDB(filepath)
    hash = hashing.md5(password)
    query = Query()
    result = db.search(query.type == 'inner_auth')
    db.close()
    if not result or len(result) == 0:
        encrypt(filepath, password)
        return False
    encrypt(filepath, password)
    return result[0]['value'] == hash

def encrypt(filepath: str, password: str):
    key = hashing.to_fernet_key(password)
    fernet = Fernet(key)
    with open(filepath, 'rb') as file:
        data = file.read()
        file.close()
    encrypted_data = fernet.encrypt(data)
    with open(filepath, 'wb') as file:
        file.write(encrypted_data)
        file.close()

def decrypt(filepath: str, password: str):
    key = hashing.to_fernet_key(password)
    fernet = Fernet(key)
    try:
        with open(filepath, 'rb') as file:
            encrypted_data = file.read()
            file.close()
        decrypted_data = fernet.decrypt(encrypted_data)
        with open(filepath, 'wb') as file: # remove a extensão .encrypted
            file.write(decrypted_data)
            file.close()
    except InvalidToken as e:
        print("Error: InvalidToken - The provided key is incorrect or the data is corrupted.", e)
        return False
    except Exception as e:
        print("An unexpected error occurred during decryption: ", e)
        return False
    return True