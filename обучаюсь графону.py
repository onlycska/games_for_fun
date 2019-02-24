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

    def init_main(self):
        toolbar = tk.Frame(bg="#000000", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        # TODO self.add_img = tk.PhotoImage(file="add.gif")
        tree = Main.tree_creation(self)
        btn_open_dlg = tk.Button(toolbar, text="+/- пользователь", command=lambda: Child().add_guest(),
                                 bg="#FFCFFF", bd=0, compound=tk.TOP)
        btn_open_dlg.pack(side=tk.LEFT)
        btn_open_dlg = tk.Button(toolbar, text="Добавить тусу",
                                 command=lambda: Child().add_hype(Main.find_available_guests()[1]),
                                 bg="#AFCFFF", bd=0, compound=tk.TOP)
        btn_open_dlg.pack(side=tk.LEFT)
        btn_open_dlg = tk.Button(toolbar, text="Обновить таблицу", command=lambda: Main.tree_creation(self, tree),
                                 bg="#FFCFFF", bd=0, compound=tk.TOP)
        btn_open_dlg.pack(side=tk.LEFT)
        # Main.view_records(self)

    def tree_creation(self, tree=None):
        # TODO обновляется список только единожды - для многоразовости нужно сделать автообновляемую переменную
        if tree is None:
            print(1)
            pass
        else:
            # print(tree.values())
            # print(row)
            tree.destroy()
            print(2)
        height_inc = len(Main.find_available_guests()[0])
        tree = ttk.Treeview(self, column=("Name", "Debt"), height=height_inc, show="headings")
        tree.column("Name", width=365, minwidth=365, stretch=True, anchor=tk.CENTER)
        tree.column("Debt", width=280, minwidth=280, stretch=True, anchor=tk.CENTER)
        tree.heading("Name", text="Имя")
        tree.heading("Debt", text="Долг")
        tree.pack()
        Main.view_records(tree)
        tree.update()
        return tree

    @staticmethod
    def view_records(tree):
        [tree.delete(i) for i in tree.get_children()]
        guests = Main.find_available_guests()[0]
        [tree.insert("", "end", values=row) for row in guests]
        # tree.destroy()

    @staticmethod
    def find_available_guests():
        available_guests_names = []
        guests = []
        available_guests = hookah_users_db.find({})
        guest_names = []
        for available_guest in available_guests:
            guest_names.append(available_guest["name"])
            available_guests_names.append(available_guest["name"])
            available_guests_names.append(available_guest["price"])
            guests.append(available_guests_names)
            available_guests_names = []
        return guests, guest_names

    @staticmethod
    def find_available_tobaccos():
        available_tobaccos_names = []
        tobaccos = []
        available_tobaccos = tobaccos_db.find({})
        tobacco_names = []
        for available_tobacco in available_tobaccos:
            tobacco_names.append(available_tobacco["name"])
            available_tobaccos_names.append(available_tobacco["name"])
            available_tobaccos_names.append(available_tobacco["price"])
            tobaccos.append(available_tobaccos_names)
            available_tobaccos_names = []
        return tobaccos, tobacco_names


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app

    def add_guest(self):
        self.title("Добавление пользователя")
        self.geometry("200x150+400+300")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        window_description = ttk.Label(self, text="Введите уже существующее имя,\nчтобы удалить гостя, или новое,\n"
                                                  "чтобы добавить.")
        window_description.pack()
        new_guest = ttk.Label(self, text="Имя гостя: ")
        new_guest.place(x=60, y=60)
        guest_name = ttk.Entry(self)
        guest_name.place(x=35, y=80)

        def user_comparison(self, new_guest):
            exist_guests = hookah_users_db.find({})
            for exist_guest in exist_guests:
                if new_guest == exist_guest["name"]:
                    Child.del_user(self, exist_guest["name"])
                    break
            else:
                Child.add_user(self, new_guest)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=115, y=120)
        btn_add = ttk.Button(self, text="Добавить", command=lambda: user_comparison(self, guest_name.get()))
        btn_add.place(x=40, y=120)

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

    def del_user(self, guest_name):
        self.destroy()
        hookah_users_db.delete_one({"name": guest_name})
        Child.window("пользователь\n удалён", "black")

    def add_user(self, guest_name):
        try:
            self.destroy()
            if guest_name == "":
                raise TypeError
            elif re.match(r"^[a-zA-Zа-яА-Я0-9]+$", guest_name) is None:
                raise TypeError
            hookah_users_db.insert_one({"name": guest_name, "price": 0.00})
            Child.window("пользователь\n успешно добавлен", "black")
        except TypeError:
            Child.window(text="это не \nподходящее имя", color="red")

    def add_hype(self, guests):
        available_tobbacos = Main.find_available_tobaccos()[1]
        window_height_coefficient = len(available_tobbacos) if len(available_tobbacos)>len(guests) else len(guests)
        self.title("Добавление тусы")
        height_inc = 30
        height = 60 + height_inc * window_height_coefficient
        height2 = 60 + height_inc * len(available_tobbacos)
        self.geometry("200x"+str(height)+"+400+300")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        Child.add_hype_guests(self, guests, height, height_inc)

    def add_hype_guests(self, guests, height, height_inc):
        label_sum = ttk.Label(self, text="Выберите, кто из гостей курил: ")
        label_sum.place(x=5, y=5)
        label_place_y = 0
        check = []
        for guest in guests:
            label_place_y += height_inc
            label_sum = ttk.Label(self, text=guest + ": ")
            label_sum.place(x=5, y=label_place_y)
            check_var = tk.BooleanVar()
            check.append(check_var)
            entry_dscrpt = ttk.Checkbutton(self, variable=check_var)
            entry_dscrpt.place(x=160, y=label_place_y)

        btn_cancel = ttk.Button(self, text="Закрыть", command=lambda: self.destroy())
        btn_cancel.place(x=115, y=height-30)
        btn_add = ttk.Button(self, text="Далее", command=lambda: Child.printer(guests, check))
        btn_add.place(x=40, y=height-30)

    @staticmethod
    def printer(guest, checker):
        guests = Main.find_available_guests()[1]
        for i in range(len(guests)):
            if not checker[i].get():
                pass
            else:
                print(guest[i], end=" ")
                print(checker[i].get())

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
            Child().add_guest()

        btn_ok = ttk.Button(window, text="Ок", command=lambda: btn_press(window))
        btn_ok.pack()


if __name__ == "__main__":
    # подключение к бд с данными о прошлых тусах
    connect = base64.standard_b64decode("bW9uZ29kYjovL2hvb2thaDoxMzAzOTdvbGVnQGRz"
                                        "MjQ3MjIzLm1sYWIuY29tOjQ3MjIzL29ubHljc2th")
    connect = connect.decode('utf-8')
    client = MongoClient(connect)
    db = client["onlycska"]
    events = db["events"]
    tobaccos_db = db["tobaccos"]
    hookah_users_db = db["guests"]
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Hookah price")
    root.geometry("650x400+300+200")
    root.resizable(True, True)
    root.mainloop()
