from tkinter import *
import train as tn
import sqlite3

# class safhe asli
class Trainreserve:
    def __init__(self, master):
        self.master = master
        myframe = Frame(master)
        myframe.grid()
        master.title('Train ticket reservation')
        master.configure(background='black')
        master.geometry('500x500')

        self.label1 = Label(master, text='Please enter the begining city:', bg='black', fg='white')
        self.label1.grid(row=0, column=0)
        self.begining = Entry(master, width=20, bg='white')
        self.begining.grid(row=0, column=1)
        self.lable2 = Label(master, text='Please enter the destination city:', bg='black', fg='white').grid(row=2, column=0)
        self.destination = Entry(master, width=20, bg='white')
        self.destination.grid(row=2, column=1)

        self.button1 = Button(master, text='SUBMIT', width=6, command=self.traininfo).grid(row=4, column=0)

        self.label3 = Label(master, text='Trains with the infromation entered:', bg='black', fg='white').grid(row=5, column=0)

        self.output = Text(master, width=75, height=6, background='white')
        self.output.grid(row=6, column=0, columnspan=4)

        self.label4 = Label(master, text='Do you want to book a ticket of this train?', bg='black', fg='white').grid(row=7, column=0)
        self.button2 = Button(master, text='YES', width=6,command=self.openNewWindow).grid(row=8, column=0)

    def traininfo(self): # etelaate train haro migire va ba sakhtar behtar dar khoruji namayesh mide
        global awns
        start = self.begining.get().strip().lower().capitalize() # pak kardan space haye ezafi, kuchak kardan hame horuf va capitalize kardan harf aval
        end = self.destination.get().strip().lower().capitalize()
        self.output.delete('0.0', END)
        connection = sqlite3.connect('trains.sqlite3')
        crsr = connection.cursor()

        crsr.execute(f'SELECT * FROM train WHERE begining="{start}" AND destination="{end}"')
        result = crsr.fetchall()
        if not result:
            oput = f'Unfortunately, there is no train from {start} to {end}!'
        else:
            awns = tn.Train(result[0])
            oput = f'ID: {awns.id}\nFrom: {awns.begining}\nDestination: {awns.destination}\nSeats remaining: {awns.seats}\nPrice per seat: {awns.price}\nDate and time: {awns.date} at {awns.time}'
        self.output.insert(END ,oput)

    def openNewWindow(self):
        self.openNewWindow = Toplevel(self.master)
        self.app = buySection(self.openNewWindow)

# class safhe kharid
class buySection:
    def __init__(self, master):
        self.master = master
        master.title(f"master train from {awns.begining} to {awns.destination}")
        master.configure(background='black')
        master.geometry("500x500")

        self.lable1 = Label(master, text='First name:', bg='black', fg='white').grid(row=1, column=0)
        self.firstname = Entry(master, width=20, bg='white')
        self.firstname.grid(row=1, column=2)
        self.lable2 = Label(master, text='Last name:', bg='black', fg='white').grid(row=2, column=0)
        self.lastname = Entry(master, width=20, bg='white')
        self.lastname.grid(row=2, column=2)
        self.lable3 = Label(master, text='Phone number:', bg='black', fg='white').grid(row=3, column=0)
        self.phonenumber = Entry(master, width=20, bg='white')
        self.phonenumber.grid(row=3, column=2)
        self.lable4 = Label(master, text='How many seats do want to book:', bg='black', fg='white').grid(row=4, column=0)
        self.seatsnum = Entry(master, width=20, bg='white')
        self.seatsnum.grid(row=4, column=2)
        self.button1 = Button(master, text='SUBMIT', width=6, command=self.price).grid(row=6, column=0)

        self.lable5 = Label(master, text='Tottal price is:', bg='black', fg='white').grid(row=7, column=0)

        self.output = Text(master, width=20, height=3, background='white')
        self.output.grid(row=8, column=0, columnspan=4)

        self.lable6 = Label(master, text='To buy tickets click on Pay', bg='black', fg='white').grid(row=9, column=0)
        self.button2 = Button(master, text='PAY', width=6, command=self.pay).grid(row=9, column=1)

    def price(self):
        try:
            self.num = int(self.seatsnum.get())
            if self.num > awns.seats: # age tedad bilit haye darkhasti bishtar az bilit haye mojud bashad elam mikonad
                oput = f'There is not enough seats! Try decreasing your number!'
            else:
                oput = f'{self.num * awns.price} Toman'
        except ValueError: # agar dar ghesmate tedad bilit bejaye number, horufe alphabet estefade shavad ekhtar midahad
            Label(self.master, text='Only number is allowed in price field!', bg='black', fg='red').grid(row=5, column=0)
        self.output.delete('0.0', END)
        self.output.insert(END ,oput)

    def pay(self):
        first = self.firstname.get().strip().lower().capitalize()
        last = self.lastname.get().strip().lower().capitalize()
        num = self.phonenumber.get()
        seat = int(self.seatsnum.get())
        connection = sqlite3.connect('trains.sqlite3')
        crsr = connection.cursor()

        crsr.execute(f'INSERT INTO reserved VALUES("{first}", "{last}", "{num}", "{awns.begining}", "{awns.destination}", {awns.id}, {seat})')
        connection.commit()
        crsr.execute(f'UPDATE train SET seats={awns.seats - seat} WHERE id={awns.id}') # tedade bilit kharidari shode ra az tedad bilit mojud kam mikonad
        connection.commit()
        self.lable7 = Label(self.master, text='You booked the tickets successfully!', bg='black', fg='red').grid(row=11, column=0)



