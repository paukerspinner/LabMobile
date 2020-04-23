from py3o.template import Template
import os
from lib.objects import *
import lib.cdr as cdr
from lib.traffic import Traffic

phoneNumber = int(input("Вводите номер телефона: "))
ipAddress = input("Вводите IP аддресс: ")

''' Создать образец '''
t = Template("template/invoice_for_payment.odt", "invoice.odt")

''' Добавлять основные информации о банке, документе, клиете, поставщике '''
bank = Bank('AO Паукер банк Г.Санкт-Петербург', '256987456', '2568521469800000550')

provider = Provider('ООО "ТКА"', '7895412652', '789541005', '6328521410500006982')
provider.setInfo('197022, Санкт-Петербург, Вяземский переулок, дом 5-7', '933863258')

document = Document('50', '20.10.2019', '№ 20036589 от 10.01.2020')

client = Client('ООО "Тесс"', '5896354128', '268942578', '197022, Санкт-Петербург, Малый проспект, дом 40', '923545265')

''' Добавлять услуги '''
items = list()
# Услуг “Телефония”
callTotal = cdr.getSmsAndCallingBill(phoneNumber)[1]
items.append(Item(1, 'Услуг “Телефония”', None, None, callTotal, callTotal))
# Услуг “CMC”
smsTotal = cdr.getSmsAndCallingBill(phoneNumber)[0]
items.append(Item(2, 'Услуг “CMC”', None, None, smsTotal, smsTotal))
# Услуг “Интернет”
tf = Traffic(ipAddress)
items.append(Item(3, 'Услуг “Интернет”', tf.calculateTraffic(), 'Кб', 1.5, tf.calculateTarrif()))

''' Добавлять счет '''
total = callTotal + smsTotal + tf.calculateTarrif()
bill = Bill(3, total, 18)

''' Встраивать данные в образце '''
data = dict(bank=bank, provider=provider, document=document, client=client, items=items, bill=bill)
t.render(data)

''' Конвертировать в PDF '''
os.system('libreoffice --headless --convert-to pdf invoice.odt')
os.system('rm -rf invoice.odt')

print('Формирование счета на оплату УСПЕШНО ВЫПОЛНЕНО!')
