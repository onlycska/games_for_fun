#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
import base64
import re


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        # TODO self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg="#000000", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        # TODO self.add_img = tk.PhotoImage(file="add.gif")
        btn_open_dlg = tk.Button(toolbar, text="Добавить пользователя", command=lambda: Child().add_guest(),
                                 bg="#FFCFFF", bd=0, compound=tk.TOP)
        btn_open_dlg.pack(side=tk.LEFT)
        btn_open_dlg = tk.Button(toolbar, text="Добавить тусу", command=lambda: Child().add_hype(guest_names),
                                 bg="#FFCFFF", bd=0, compound=tk.TOP)
        btn_open_dlg.place(x=139)
        self.tree = ttk.Treeview(self, column=("Name", "Debt"), height=15, show="headings")
        self.tree.column("Name", width=365, anchor=tk.CENTER)
        self.tree.column("Debt", width=280, anchor=tk.CENTER)
        self.tree.heading("Name", text="Имя")
        self.tree.heading("Debt", text="Долг")
        self.tree.pack()

    # def records(self, description, costs, total):
    #     # TODO self.db.insert_data(description, costs, total)
    #     self.view_records()

    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in guests]


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        # self.init_child()
        self.view = app

    def add_guest(self):
        self.title("Добавление пользователя")
        self.geometry("200x120+400+300")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        label_sum = ttk.Label(self, text="Имя гостя: ")
        label_sum.place(x=60, y=30)
        guest_name = ttk.Entry(self)
        guest_name.place(x=35, y=50)
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=115, y=90)
        btn_add = ttk.Button(self, text="Добавить", command=lambda: Child.add_user(self, guest_name.get()))
        btn_add.place(x=40, y=90)

        # код на случай чего
        # label_dscrptn = ttk.Label(self, text="Наименование:")
        # label_dscrptn.place(x=50, y=50)
        # label_slctn = ttk.Label(self, text="Статья дохода/расхода:")
        # label_slctn.place(x=50, y=80)
        # check_var = tk.BooleanVar()
        # self.entry_dscrpt = ttk.Checkbutton(self, variable=check_var)
        # self.entry_dscrpt.pack()
        # self.entry_dscrpt.place(x=200, y=50)
        # self.combobox = ttk.Combobox(self, values=[u"Доход", u"Расход"])
        # self.combobox.current(0)
        # self.combobox.place(x=200, y=80)

    def add_user(self, guest_name):
        try:
            self.destroy()
            if guest_name == "":
                raise TypeError
            elif re.match(r"^[a-zA-Zа-яА-Я0-9]+$", guest_name) is None:
                raise TypeError
            # hookah_users.insert_one({"name": self.entry_money.get(), "price": 0.00})
            Child.window("пользователь\n успешно добавлен", "black")
        except TypeError:
            Child.window(text="это не \nподходящее имя", color="red")

    def add_hype(self, guests):
        self.title("Добавление тусы")
        self.geometry("200x620+400+300")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        y1 = 0
        check = []
        for guest in guests:
            y1 += 50
            label_sum = ttk.Label(self, text=guest + ": ")
            label_sum.place(x=5, y=y1)
            check_var = tk.BooleanVar()
            check.append(check_var.get())
            entry_dscrpt = ttk.Checkbutton(self, variable=check_var)
            entry_dscrpt.place(x=60, y=y1)
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=115, y=590)
        btn_add = ttk.Button(self, text="Добавить", command=lambda: Child.printer(guests, check))
        btn_add.place(x=40, y=590)

    @staticmethod
    def printer(guest, checker):
        for i in range(len(guests)):
            if not checker[i]:
                print(checker[i])
                pass
            else:
                print(guest[i], end="")
                print(checker[i])

    @staticmethod
    def window(text, color):
        window = tk.Toplevel()
        window.title("Операция выполнена")
        window.geometry("300x100+400+300")
        window.resizable(False, False)
        window.grab_set()
        window.focus_set()
        msg = tk.Label(window, text=text.upper(), fg=color)
        msg.pack(side=tk.TOP)

        def btn_press(wndw):
            wndw.destroy()
            Child()

        btn_ok = ttk.Button(window, text="Ок", command=lambda: btn_press(window))
        btn_ok.pack()

        # btn_add.bind("<Button-1>", lambda event: self.view.records(self.entry_dscrpt.get(),
        #                                                            self.entry_money.get(),
        #                                                            self.combobox.get()))


if __name__ == "__main__":
    # подключение к бд с данными о прошлых тусах
    connect = base64.standard_b64decode("bW9uZ29kYjovL2hvb2thaDoxMzAzOTdvbGVnQGRz"
                                        "MjQ3MjIzLm1sYWIuY29tOjQ3MjIzL29ubHljc2th")
    connect = connect.decode('utf-8')
    client = MongoClient(connect)
    db = client["onlycska"]
    events = db["events"]
    tobaccos = db["tobaccos"]
    hookah_users = db["guests"]
    available_guests_names = []
    guests = []
    count = hookah_users.count_documents({})
    available_guests = hookah_users.find({})
    guest_names = []
    for available_guest in available_guests:
        available_guests_names.append(available_guest["name"])
        guest_names.append(available_guest["name"])
        available_guests_names.append(available_guest["price"])
        guests.append(available_guests_names)
        available_guests_names = []

    root = tk.Tk()
    # TODO db = None
    app = Main(root)
    app.pack()
    root.title("Hookah price")
    root.geometry("650x400+300+200")
    root.resizable(False, False)
    root.mainloop()


# from tkinter import *
#
# root = Tk()
# root.geometry("650x450+300+200")
#
# check_var = BooleanVar()
# #check_var.set(0)
# label_state = Label(root, text='Состояние: ' + str(check_var.get()))
#
# check = Checkbutton(root, text='Текст', variable=check_var)
#
# check.pack()
# label_state.pack()
#
#
# def on_change(*args):
#     label_state.config(text='Состояние: ' + str(check_var.get()))
#
#
# def printer():
#     print(int(check_var.get()))
#
#
# check_var.trace('w', on_change)  # Следим за состоянием переменной, при изменении выполняем функцию
#
# Button(root, text='Включить', command=lambda: check_var.set(True)).pack()
# Button(root, text='Выключить', command=lambda: check_var.set(False)).pack()
# Button(root, text="Print", command=printer).pack()
#
# mainloop()
