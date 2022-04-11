import PySimpleGUI as sg
import os
import urllib.request
from xml.dom import minidom


def currency_conv(input_1, input_2, amount, curr_1_data, curr_2_data):
    # Currency conversion through rubles
    if input_1 == input_2:
        result = amount
    elif input_1 == 'RUB':
        result = amount * (int(curr_2_data[2]) / float(curr_2_data[1]))
    elif input_2 == 'RUB':
        result = amount * (float(curr_1_data[1]) / int(curr_1_data[2]))
    else:
        first_to_RUB = float(curr_1_data[1]) / int(curr_1_data[2])
        RUB_to_second = int(curr_2_data[2]) / float(curr_2_data[1])
        result = amount * first_to_RUB * RUB_to_second
    return result


def currency_data(currency_file, input_charcode):
    # Currency data extraction
    curr_data = []
    for rate in currency_file:
        charcode = rate.getElementsByTagName("CharCode")[0]
        name = rate.getElementsByTagName("Name")[0]
        value = rate.getElementsByTagName("Value")[0]
        nominal = rate.getElementsByTagName("Nominal")[0]
        if charcode.firstChild.data == input_charcode:
            curr_data = [name.firstChild.data, value.firstChild.data, nominal.firstChild.data]
            curr_data[1] = curr_data[1].replace(',', '.')
    return curr_data


url = "http://www.cbr.ru/scripts/XML_daily.asp"

# Read URL
webFile = urllib.request.urlopen(url)
data = webFile.read()
FileName = 'currency_data.xml'
with open(FileName, "wb") as localFile:
    localFile.write(data)
webFile.close()

# Parse xml
doc = minidom.parse(FileName)

# Data extraction
root = doc.getElementsByTagName("ValCurs")[0]
date = "Конвертация по курсу валют ЦБ РФ \nна {date}г".format(date=root.getAttribute('Date'))

# Currency list extraction
currency = doc.getElementsByTagName("Valute")

curr_list = []
for rate in currency:
    charcode = rate.getElementsByTagName("CharCode")[0]
    curr_list.append(charcode.firstChild.data)
curr_list.append('RUB')
curr_list.sort()

# Create the elements
layout = [[sg.Text(date, font='Colibri 14', background_color='green')],
          [sg.Text("Первая валюта", font='Colibri 14', background_color='green'),
           sg.Combo(curr_list, key='input_1', font='Colibri 12', size=(5, 1), readonly=True),
           sg.InputText('', key='amount', size=(15, 1))],
          [sg.Text("Вторая валюта", font='Colibri 14', background_color='green'),
           sg.Combo(curr_list, key='input_2', font='Colibri 12', size=(5, 1), readonly=True),
           sg.InputText('', key='result', size=(15, 1), readonly=True)],
          [sg.Button('OK', key='OK', font='Colibri 12', border_width=5),
           sg.Button('Cancel', key='Cancel', font='Colibri 12', border_width=5)]]

# Create the Window
window = sg.Window('Currency Converter', layout, size=(350, 180), background_color='green')

# Create the event loop
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        # User closed the Window or hit the Cancel button
        break

    if event == 'OK':
        input_1 = values['input_1']
        input_2 = values['input_2']
        amount = values['amount']
        if ',' in amount:
            amount = amount.replace(',', '.')
        amount = float(amount)

        # Currency data extraction
        curr_1_data = currency_data(currency, input_1)
        curr_2_data = currency_data(currency, input_2)

        # Currency conversion
        conv_res = currency_conv(input_1, input_2, amount, curr_1_data, curr_2_data)

        window['result'].update(str(round(conv_res, 2)))
window.close()
os.remove('currency_data.xml')

