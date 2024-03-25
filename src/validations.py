def open_vault_validation(filepath: str, password: str):
    if not filepath or filepath == '':
        return {'error': 'NO_FILE'}
    return True

def password_validation(password: str, password_confirmation: str):
    if not password or not password_confirmation:
        return {'error': 'NO_PASSWORD'}
    if password == '' or password_confirmation == '':
        return {'error': 'NO_PASSWORD'}
    return password == password_confirmation

def vault_data_validation(vault_path: str, vault_name: str):
    if not vault_path or vault_path == '':
        return {'error': 'NO_VAULT_PATH'}
    if not vault_name or vault_name == '':
        return {'error': 'NO_VAULT_NAME'}
    return True

def insert_password_validation(name: str, username: str, password: str):
    if not name or name == '':
        return {'error': 'NO_NAME'}
    if not username or username == '':
        return {'error': 'NO_USERNAME'}
    if not password or password == '':
        return {'error': 'NO_PASSWORD'}
    return True

def map_error(error: str):
    match error:
        case 'NO_PASSWORD':
            return 'Password is required'
        case 'NO_VAULT_PATH':
            return 'Vault path is required'
        case 'NO_VAULT_NAME':
            return 'Vault name is required'
        case 'NO_FILE':
            return 'Please select a vault file'
        case 'NO_NAME':
            return 'Name is required'
        case 'NO_USERNAME':
            return 'Username is required'
