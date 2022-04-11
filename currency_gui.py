import PySimpleGUI as sg

curr_list = ['USD', 'EUR', 'RUB']
# Create the elements
layout = [[sg.Text("Выберите первую валюту", font='Colibri 14', background_color='green'), sg.Combo(curr_list, key='input_1', font='Colibri 12', size=(5, 1))],
          [sg.Text('Сумма конвертации', font='Colibri 13', background_color='green'), sg.InputText('', key='amount', size=(15, 1))],
          [sg.Text("Выберите вторую валюту", font='Colibri 14', background_color='green'), sg.Combo(curr_list, key='input_2', font='Colibri 12', size=(5, 1))],
          [sg.Text('Сумма результат', font='Colibri 13', background_color='green'), sg.InputText('', key='result', size=(15, 1))],
          [sg.Button('OK', font='Colibri 12', border_width=5),
           sg.Button('Cancel', font='Colibri 12', border_width=5)]]

# Create the Window
window = sg.Window('Currency Converter', layout, size=(350, 180), background_color='green')

# Create the event loop
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        # User closed the Window or hit the Cancel button
        break
    print(f'Event: {event}')
    print(values)

    # window['Сумма результат'].update(str(result))
window.close()
