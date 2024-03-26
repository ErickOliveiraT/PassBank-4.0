import PySimpleGUI as sg

def new_vault(window: sg.Window):
    window['MAIN'].update(visible=False)
    window['CREATE_VAULT'].update(visible=True)
    return

def main_menu(window: sg.Window):
    window['MAIN'].update(visible=True)
    window['CREATE_VAULT'].update(visible=False)
    return

def insert_password(window: sg.Window):
    window['VAULT_OPENED'].update(visible=False)
    window['PASSWORDS_VIEW'].update(visible=False)
    window['INSERT_PASSWORD'].update(visible=True)
    return

def back(window: sg.Window):
    window['INSERT_PASSWORD'].update(visible=False)
    window['VAULT_OPENED'].update(visible=True)
    return

def list_passwords(window: sg.Window):
    window['VAULT_OPENED'].update(visible=False)
    window['PASSWORDS_VIEW'].update(visible=True)
    return

def vault_opened(window: sg.Window):
    window['MAIN'].update(visible=False)
    window['INSERT_PASSWORD'].update(visible=False)
    window['VAULT_OPENED'].update(visible=True)
    return