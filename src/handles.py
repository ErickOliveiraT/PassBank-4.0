import PySimpleGUI as sg
import validations
import navigation
import passwords
import pyperclip
import vault

def vault_creation(values: dict):
    vault_validation = validations.vault_data_validation(values['vault_path'], values['vault_name'])
    if type(vault_validation) == dict and vault_validation['error']:
        sg.popup(validations.map_error(vault_validation['error']))
    elif type(vault_validation) == bool and vault_validation:
        pass_validation = validations.password_validation(values['password1'], values['password_confirmation'])
        if type(pass_validation) == dict and pass_validation['error']:
            sg.popup(validations.map_error(pass_validation['error']))
        elif type(pass_validation) == bool and not pass_validation:
            sg.popup('Passwords do not match')
        elif type(pass_validation) == bool and pass_validation:
            vault.create(values['vault_path'], values['vault_name'], values['password1'])
            sg.popup('Vault created')

def password_insertion(values: dict, password: str):
    insert_validation = validations.insert_password_validation(values['name'], values['username'], values['reg_password'])
    if type(insert_validation) == dict and insert_validation['error']:
        sg.popup(validations.map_error(insert_validation['error']))
    else:
        insert_res = passwords.insert(values['filepath'], password, values['name'], values['username'], values['reg_password'], values['description'])
        if not insert_res:
            sg.popup('Error inserting data')
        else:
            sg.popup('Data inserted')

def vault_opening(window: sg.Window, values: dict):
    open_validation = validations.open_vault_validation(values['filepath'], values['password'])
    if type(open_validation) == dict and open_validation['error']:
        sg.popup(validations.map_error(open_validation['error']))
    else:
        auth_res = vault.auth(values['filepath'], values['password'])
        if not auth_res:
            sg.popup('Invalid password or vault file')
        else:
            navigation.vault_opened(window)
            return values['password']

def list_passwords(window: sg.Window, values: dict, password: str):
    passwords_data = passwords.get(values['filepath'], password)
    passwords_table = [[x['name'], x['description'], x['username'], x['password']] for x in passwords_data]
    window['passwords_table'].update(values=passwords_table)
    return passwords_table

def table_click(event: tuple, passwords_table: list):
    coords = event[2]
    if coords[1] > 1:
        cell = passwords_table[coords[0]][coords[1]]
        pyperclip.copy(cell)
    return

def show_passwords(window: sg.Window, event: str, values: dict):
    match event:
        case 'show_password':
            window['password'].update(password_char='' if values['show_password'] else '*')
            return
        case 'show_password_confirmation':
            window['password_confirmation'].update(password_char='' if values['show_password_confirmation'] else '*')
            return
        case 'show_password2':
            window['password1'].update(password_char='' if values['show_password2'] else '*')
            return
        case 'show_reg_password':
            window['reg_password'].update(password_char='' if values['show_reg_password'] else '*')
            return
    return