import urllib.request
from xml.dom import minidom

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

NOK = []  # Данные по норвежским кронам
HUF = []  # Данные по венгерским форинтам
for rate in currency:
    charcode = rate.getElementsByTagName("CharCode")[0]
    name = rate.getElementsByTagName("Name")[0]
    value = rate.getElementsByTagName("Value")[0]
    nominal = rate.getElementsByTagName("Nominal")[0]
    if charcode.firstChild.data == 'NOK':
        NOK = [name.firstChild.data, value.firstChild.data, nominal.firstChild.data]
    elif charcode.firstChild.data == 'HUF':
        HUF = [name.firstChild.data, value.firstChild.data, nominal.firstChild.data]

NOK[1] = NOK[1].replace(',', '.')
HUF[1] = HUF[1].replace(',', '.')

# Конвертация валют

# NOK_to_RUB = float(NOK[1]) / int(NOK[2])
# RUB_to_HUF = int(HUF[2]) / float(HUF[1])
# NOK_to_HUF = NOK_to_RUB * RUB_to_HUF
#
# print(date)
# print(f'1 {NOK[0]} = {round(NOK_to_HUF, 2)} {HUF[0]}')

HUF_to_RUB = float(HUF[1]) / int(HUF[2])
RUB_to_NOK = int(NOK[2]) / float(NOK[1])

convert_sum = float(input('Введите сумму в венгерских форинтах: '))
result = convert_sum * HUF_to_RUB * RUB_to_NOK

print(date)
print(f'{convert_sum} венгерских форинтов = {round(result, 2)} норвежских крон')
