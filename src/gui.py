import PySimpleGUI as sg
import validations
import passwords
import pyperclip
import vault

# Layouts
start = [
    [sg.Text('Open vault'), sg.Input(key='filepath', ), sg.FileBrowse()],
    [sg.Text('Password'), sg.Input(key='password', password_char='*'), sg.Checkbox('Show password', key='show_password', enable_events=True)],
    [sg.Button('Open'), sg.Button('Create new Vault'), sg.Button('Exit')]
]

vault_creation = [
    [sg.Text('Vault location'), sg.Input(key='vault_path'), sg.FolderBrowse()],
    [sg.Text('Vault name'), sg.Input(key='vault_name', )],
    [sg.Text('Password'), sg.Input(key='password', password_char='*'), sg.Checkbox('Show password', key='show_password', enable_events=True)],
    [sg.Text('Confirm Password'), sg.Input(key='password_confirmation', password_char='*'), sg.Checkbox('Show password', key='show_password_confirmation', enable_events=True)],
    [sg.Button('Create Vault'), sg.Button('Main Menu')]
]

vault_opened = [
    [sg.Button('Insert new password'), sg.Button('List passwords'), sg.Button('Exit')]
]

password_insertion = [
    [sg.Text('Name'), sg.Input(key='name')],
    [sg.Text('Username'), sg.Input(key='username')],
    [sg.Text('Password'), sg.Input(key='reg_password', password_char='*'), sg.Checkbox('Show password', key='show_reg_password', enable_events=True)],
    [sg.Text('Description'), sg.Input(key='description')],
    [sg.Button('Insert'), sg.Button('Back')]
]

passwords_view = [
    [sg.Table([], headings=["Name", "Description", "Username", "Password"], key="passwords_table", enable_click_events=True, auto_size_columns=True)],
    [sg.Button('Insert new password'), sg.Button('Exit')]
]

layout = [[
    sg.Column(start, key='MAIN'), 
    sg.Column(vault_creation, visible=False, key='CREATE_VAULT'),
    sg.Column(vault_opened, visible=False, key='VAULT_OPENED'),
    sg.Column(password_insertion, visible=False, key='INSERT_PASSWORD'),
    sg.Column(passwords_view, visible=False, key='PASSWORDS_VIEW')
]]

# Globals
window = sg.Window('PassBank 4.0', layout)
password = False

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if type(event) == tuple and event[0] == 'passwords_table' and event[1] == '+CLICKED+':
        coords = event[2]
        if coords[1] > 1:
            cell = passwords_table[coords[0]][coords[1]]
            pyperclip.copy(cell)
    elif event == sg.WIN_CLOSED or event.startswith('Exit'):
        break
    elif event == 'List passwords':
        window['VAULT_OPENED'].update(visible=False)
        window['PASSWORDS_VIEW'].update(visible=True)
        passwords_data = passwords.get(values['filepath'], password)
        passwords_table = [[x['name'], x['description'], x['username'], x['password']] for x in passwords_data]
        window['passwords_table'].update(values=passwords_table)
    elif event == 'Open':
        open_validation = validations.open_vault_validation(values['filepath'], values['password'])
        if type(open_validation) == dict and open_validation['error']:
            sg.popup(validations.map_error(open_validation['error']))
        else:
            auth_res = vault.auth(values['filepath'], values['password'])
            if not auth_res:
                sg.popup('Invalid password or vault file')
            else:
                password = values['password']
                window['MAIN'].update(visible=False)
                window['VAULT_OPENED'].update(visible=True)
    elif event == 'Insert':
        insert_validation = validations.insert_password_validation(values['name'], values['username'], values['reg_password'])
        if type(insert_validation) == dict and insert_validation['error']:
            sg.popup(validations.map_error(insert_validation['error']))
        else:
            insert_res = passwords.insert(values['filepath'], password, values['name'], values['username'], values['reg_password'], values['description'])
            if not insert_res:
                sg.popup('Error inserting data')
            else:
                sg.popup('Data inserted')
    elif event == 'Back':
        window['INSERT_PASSWORD'].update(visible=False)
        window['VAULT_OPENED'].update(visible=True)
    elif event.startswith('Insert new password'):
        window['VAULT_OPENED'].update(visible=False)
        window['PASSWORDS_VIEW'].update(visible=False)
        window['INSERT_PASSWORD'].update(visible=True)
    elif event == 'Create new Vault':
        password = False
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
    elif event == 'show_reg_password':
        window['reg_password'].update(password_char='' if values['show_reg_password'] else '*')
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