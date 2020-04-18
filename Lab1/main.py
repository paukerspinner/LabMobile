# on Ubuntu, requires install: `sudo apt-get install -y python3-tk`
import tkinter as tk
import requests
import pandas
import cdr

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.database = 'data.csv'
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        ''' Left Frame '''
        self.frLeft = tk.Frame(self)
        self.frLeft.grid(row=1, column=1)

        self.frTelNumber = tk.Frame(self.frLeft, width=20)
        self.frTelNumber.pack(padx=5, pady=5)

        self.labelTelNumber = tk.Label(self.frTelNumber, text='Тел.')
        self.labelTelNumber.pack(side='left')

        self.txtTelNumber = tk.Text(self.frTelNumber, height=1, width=15)
        self.txtTelNumber.insert('1.0', '933156729')
        self.txtTelNumber.pack()

        self.btShowBilling = tk.Button(self.frLeft, text='Тарификация', width=20)
        self.btShowBilling["command"] = self.showBilling
        self.btShowBilling.pack(padx=5, pady=5)

        self.btShowRecords = tk.Button(self.frLeft, text='Мои записи', width=20)
        self.btShowRecords['command'] = self.showRecords
        self.btShowRecords.pack(padx=5, pady=5)

        self.btShowTariff = tk.Button(self.frLeft, text='Мой тариф', width=20)
        self.btShowTariff['command'] = self.showTariff
        self.btShowTariff.pack(padx=5, pady=5)

        ''' Right Frame '''
        self.frRight = tk.Frame(self)
        self.frRight.grid(row=1, column=2)

        self.content = tk.Text(self.frRight, height = 20)
        self.content.pack(padx=5)

    def showRecords(self):
        try:
            telNum = int(self.txtTelNumber.get('1.0', 'end-1c'))
        except ValueError:
            self.content.insert('1.0', 'Проверьте номер телефона, пожалуйста!\n--------------*******--------------\n\n')
            return

        dt = pandas.read_csv(self.database)
        originRecords, destRecords = cdr.getRecords(telNum, dt.values)
        
        text = 'ЗАПИСИ:\n'
        text += '%s <> %s <> %s <> %s <> %s' % ('timestamp', 'msisdn_origin', 'msisdn_dest', 'call_duration', 'sms_number')
        for rc in originRecords + destRecords:
            text += '\n' + rc.toString()
        endline = '\n--------------*******--------------\n\n'
        self.content.insert('1.0', text + endline)

    def showTariff(self):
        info = 'ТАРИФ:\n2руб/минута исходящие звонки первые 10минут, далее 0руб/минута, 4руб/минута входящие\nсмс - 0руб/шт первые 10, далее 5руб/шт'
        endline = '\n--------------*******--------------\n\n'
        self.content.insert('1.0', info + endline)

    def showBilling(self):
        try:
            telNum = int(self.txtTelNumber.get('1.0', 'end-1c'))
        except ValueError:
            self.content.insert('1.0', 'Проверьте номер телефона, пожалуйста!\n--------------*******--------------\n\n')
            return

        text = 'ТАРИФИКАЦИЯ:\n'
        dt = pandas.read_csv(self.database)
        smsBill, outgoingBill, incomingBill = cdr.tariffing(telNum, dt.values)
        text += 'СМС: %d руб.\nИсходящие звонки: %d руб.\nВходящие звонки: %d руб.\nИтого: %d руб.' \
                    % (smsBill, outgoingBill, incomingBill, sum([smsBill, outgoingBill, incomingBill]))
        endline = '\n--------------*******--------------\n\n'
        self.content.insert('1.0',text + endline)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.master.title("Обработка и тарификация CDR")
    app.mainloop()