import PySimpleGUI as sg
import validations
import vault

# Layouts
start = [[sg.Text('Open vault'), sg.Input(key='filepath', ), sg.FileBrowse()],
        [sg.Text('Password'), sg.Input(key='password', password_char='*'), sg.Checkbox('Show password', key='show_password', enable_events=True)],
        [sg.Button('Open'), sg.Button('Create new Vault'), sg.Button('Exit')] ]

vault_creation = [[sg.Text('Vault location'), sg.Input(key='vault_path', ), sg.FolderBrowse()],
        [sg.Text('Vault name'), sg.Input(key='vault_name', )],
        [sg.Text('Password'), sg.Input(key='password', password_char='*'), sg.Checkbox('Show password', key='show_password', enable_events=True)],
        [sg.Text('Confirm Password'), sg.Input(key='password_confirmation', password_char='*'), sg.Checkbox('Show password', key='show_password_confirmation', enable_events=True)],
        [sg.Button('Create Vault'), sg.Button('Main Menu')] ]

layout = [[sg.Column(start, key='MAIN'), sg.Column(vault_creation, visible=False, key='CREATE_VAULT')]]

# Create the Window
window = sg.Window('PassBank 4.0', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Open':
        open_validation = validations.open_vault_validation(values['filepath'], values['password'])
        if type(open_validation) == dict and open_validation['error']:
            sg.popup(validations.map_error(open_validation['error']))
        else:
            auth_res = vault.auth(values['filepath'], values['password'])
            if not auth_res:
                sg.popup('Invalid password or vault file')
            else:
                sg.popup('Vault opened')
    elif event == 'Create new Vault':
        window['MAIN'].update(visible=False)
        window['CREATE_VAULT'].update(visible=True)
    elif event == 'Main Menu':
        window['MAIN'].update(visible=True)
        window['CREATE_VAULT'].update(visible=False)
    elif event == 'show_password':
        window['password'].update(password_char='' if values['show_password'] else '*')
    elif event == 'show_password_confirmation':
        window['password_confirmation'].update(password_char='' if values['show_password_confirmation'] else '*')
    elif event == 'show_password2':
        window['password1'].update(password_char='' if values['show_password2'] else '*')
    elif event == 'Create Vault':
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
    else:
        print('event:', event)
        print('values:', values)


window.close()