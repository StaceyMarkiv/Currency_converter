import os
import urllib.request
from xml.dom import minidom

input_1 = input('Введите первую валюту и сумму для конвертации: ')
input_2 = input('Введите вторую валюту: ')
input_1 = input_1.split()

url = "http://www.cbr.ru/scripts/XML_daily.asp"

# Чтение URL
webFile = urllib.request.urlopen(url)
data = webFile.read()
FileName = 'currency_data.xml'
with open(FileName, "wb") as localFile:
    localFile.write(data)
webFile.close()

# Парсинг xml
doc = minidom.parse(FileName)

# Извлечение даты
root = doc.getElementsByTagName("ValCurs")[0]
date = "\nКонвертация по курсу валют ЦБ РФ на \x1b[1;4m{date}г\x1b[0m:".format(date=root.getAttribute('Date'))

# Извлечение данных по валютам
currency = doc.getElementsByTagName("Valute")
curr_1_data = []
curr_2_data = []
for rate in currency:
    charcode = rate.getElementsByTagName("CharCode")[0]
    name = rate.getElementsByTagName("Name")[0]
    value = rate.getElementsByTagName("Value")[0]
    nominal = rate.getElementsByTagName("Nominal")[0]
    if charcode.firstChild.data == input_1[0]:
        curr_1_data = [name.firstChild.data, value.firstChild.data, nominal.firstChild.data]
        curr_1_data[1] = curr_1_data[1].replace(',', '.')
    elif charcode.firstChild.data == input_2:
        curr_2_data = [name.firstChild.data, value.firstChild.data, nominal.firstChild.data]
        curr_2_data[1] = curr_2_data[1].replace(',', '.')

# Конвертация валют
if input_1[0] == 'RUB':
    curr_1_data = ['Рубль', '1', '1']
    result = float(input_1[1]) * (int(curr_2_data[2]) / float(curr_2_data[1]))
elif input_2 == 'RUB':
    curr_2_data = ['Рубль', '1', '1']
    result = float(input_1[1]) * (float(curr_1_data[1]) / int(curr_1_data[2]))
else:
    first_to_RUB = float(curr_1_data[1]) / int(curr_1_data[2])
    RUB_to_second = int(curr_2_data[2]) / float(curr_2_data[1])
    result = float(input_1[1]) * first_to_RUB * RUB_to_second

print(date)
print(f'{input_1[1]} {curr_1_data[0]} = {round(result, 2)} {curr_2_data[0]}')

os.remove('currency_data.xml')
