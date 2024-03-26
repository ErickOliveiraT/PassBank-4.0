import PySimpleGUI as sg
import navigation
import passwords
import handles

# Layouts
start = [
    [sg.Text('Open vault'), sg.Input(key='filepath', ), sg.FileBrowse()],
    [sg.Text('Password'), sg.Input(key='password', password_char='*'), sg.Checkbox('Show password', key='show_password', enable_events=True)],
    [sg.Button('Open'), sg.Button('Create new Vault'), sg.Button('Generate Password'), sg.Button('Exit')]
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

passwords_generator = [
    [sg.Text('Password length'), sg.Spin(passwords.get_pass_length_range(), size=(7, 1), initial_value=16, key='password_length')],
    [sg.Checkbox('Uppercase', key='uppercase')],
    [sg.Checkbox('Numbers', key='numbers')],
    [sg.Checkbox('Special characters', key='special_chars')],
    [sg.Input(key='generated_password', size=(50, 1))],
    [sg.Button('Generate'), sg.Button('Copy'), sg.Button('Back')]
]

layout = [[
    sg.Column(start, key='MAIN'), 
    sg.Column(vault_creation, visible=False, key='CREATE_VAULT'),
    sg.Column(vault_opened, visible=False, key='VAULT_OPENED'),
    sg.Column(password_insertion, visible=False, key='INSERT_PASSWORD'),
    sg.Column(passwords_view, visible=False, key='PASSWORDS_VIEW'),
    sg.Column(passwords_generator, visible=False, key='PASSWORDS_GENERATOR')
]]

# Globals
window = sg.Window('PassBank 4.0', layout)
passwords_table = []
password = False

while True:
    event, values = window.read()
    if type(event) == tuple and event[0] == 'passwords_table' and event[1] == '+CLICKED+':
        handles.table_click(event, passwords_table)
    elif event == sg.WIN_CLOSED or event.startswith('Exit'):
        break
    elif event == 'List passwords':
        navigation.list_passwords(window)
        passwords_table = handles.list_passwords(window, values, password)
    elif event == 'Open':
        password = handles.vault_opening(window, values)
    elif event == 'Insert':
        handles.password_insertion(values, password)
        navigation.vault_opened(window)
    elif event == 'Back':
        navigation.back(window)
    elif event == 'Back6':
        navigation.main_menu(window)
    elif event.startswith('Insert new password'):
        navigation.insert_password(window)
    elif event == 'Create new Vault':
        navigation.new_vault(window)
    elif event == 'Main Menu':
        navigation.main_menu(window)
    elif 'show' in event and 'password' in event:
        handles.show_passwords(window, event, values)
    elif event == 'Create Vault':
        handles.vault_creation(values)
        navigation.main_menu(window)
    elif event.startswith('Generate Password'):
        navigation.password_generator(window)
    elif event == 'Generate':
        handles.generate_password(window, values)
    elif event == 'Copy':
        handles.copy_password(window)
    else:
        print('event:', event)
        print('values:', values)

window.close()