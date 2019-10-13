#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
import base64
import re
import functools


class Main(tk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.guests_tree = self.guests_tree_creation()
        self.tobaccos_tree = self.tobaccos_tree_creation()
        self.init_main()

    def init_main(self):

        self.update_table("guests")
        self.update_table("tobaccos")

        toolbar = tk.Frame(bg="#000000", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        # TODO self.add_img = tk.PhotoImage(file="add.gif")
        btn_open_dlg = tk.Button(toolbar, text="Добавить гостя", command=lambda: Child().add_guest(),
                                 bg="#FFCFFF", bd=0, compound=tk.TOP)
        btn_open_dlg.pack(side=tk.LEFT)
        btn_open_dlg = tk.Button(toolbar, text="Добавить тусу",
                                 command=lambda: Child().add_hype(Main.find_data_from_db("guests")[1]),
                                 bg="#AFCFFF", bd=0, compound=tk.TOP)
        btn_open_dlg.pack(side=tk.LEFT)
        btn_open_dlg = tk.Button(toolbar, text="Добавить табак",
                                 # command=functools.partial(Child.add_tobacco),
                                 command=lambda: Child().add_tobacco(),
                                 bg="#FFCFFF", bd=0, compound=tk.TOP)
        btn_open_dlg.pack(side=tk.LEFT)

    def guests_tree_creation(self):
        height_inc = len(Main.find_data_from_db("guests")[0])
        tree = ttk.Treeview(self, column=("Name", "Debt"), height=height_inc, show="headings")
        tree.column("Name", width=365, minwidth=365, stretch=True, anchor=tk.CENTER)
        tree.column("Debt", width=280, minwidth=280, stretch=True, anchor=tk.CENTER)
        tree.heading("Name", text="Имя")
        tree.heading("Debt", text="Долг")
        tree.pack(expand=True, fill='y')

        self.columnconfigure(5, weight=5)  # column with treeview
        self.rowconfigure(2, weight=15)  # row with treeview

        tree.bind("<Button-3>", self.context_guest_menu)
        return tree

    def update_table(self, updated_table):

        if updated_table == "guests":
            tree = self.guests_tree
            updated_list = Main.find_data_from_db("guests")[0]
        elif updated_table == "tobaccos":
            tree = self.tobaccos_tree
            updated_list = Main.find_data_from_db("tobaccos")[0]
        else:
            raise SyntaxError("Таблицы '{}' нет в используемой базе данных".format(updated_table))

        children = tree.get_children()

        if len(children) > 0:
            tree.delete(*children)

        [tree.insert("", "end", values=row) for row in updated_list]
        tree.config(height=len(updated_list))

    def tobaccos_tree_creation(self):

        height_inc = len(Main.find_data_from_db("tobaccos")[0])
        tree = ttk.Treeview(self, column=("Name", "Price"), height=height_inc, show="headings")
        tree.column("Name", width=365, minwidth=365, stretch=True, anchor=tk.CENTER)
        tree.column("Price", width=280, minwidth=280, stretch=True, anchor=tk.CENTER)
        tree.heading("Name", text="Название табака")
        tree.heading("Price", text="Цена")
        tree.pack()
        tree.bind("<Button-3>", self.context_tobacco_menu)
        return tree

    def context_guest_menu(self, event):
        context_menu = tk.Menu(self, tearoff=0)
        tree_item = ''

        def edit_guest(action):
            if tree_item:
                name_of_guest = 0
                debt = 1
                name = self.guests_tree.item(tree_item)["values"][name_of_guest]
                if action == "delete":
                    hookah_users_db.delete_one({"name": name})
                    self.update_table("guests")
                elif action == "set debt to zero":
                    if self.guests_tree.item(tree_item)["values"][debt] == "0.0":
                        pass
                    else:
                        update_user_price = {"name": name, "price": 0.0}
                        hookah_users_db.find_one_and_replace({"name": name}, update_user_price)
                        self.update_table("guests")
            else:
                Child.window(text="не выбран ни один пользователь", color="red")

        context_menu.add_command(label='Обнулить долг', command=lambda: edit_guest(action="set debt to zero"))
        context_menu.add_command(label='Удалить', command=lambda: edit_guest(action="delete"))
        context_menu.post(event.x_root, event.y_root)
        tree_item = app.guests_tree.focus()

    def context_tobacco_menu(self, event):
        context_menu = tk.Menu(self, tearoff=0)
        tree_item = ''

        def edit_guest(action):
            if tree_item:
                name_of_tobacco = 0
                name = self.tobaccos_tree.item(tree_item)["values"][name_of_tobacco]
                if action == "delete":
                    tobaccos_db.delete_one({"name": name})
                    self.update_table("tobaccos")
            else:
                Child.window(text="не выбран ни один табак", color="red")

        context_menu.add_command(label='Удалить', command=lambda: edit_guest(action="delete"))
        context_menu.post(event.x_root, event.y_root)
        tree_item = app.tobaccos_tree.focus()

    @staticmethod
    def find_data_from_db(db_data_finder):
        if db_data_finder == "guests":
            available_data = hookah_users_db.find({})
        elif db_data_finder == "tobaccos":
            available_data = tobaccos_db.find({})
        else:
            raise SyntaxError("Таблицы '{}' нет в используемой базе данных".format(db_data_finder))

        available_names = []
        names_and_values = []
        only_names = []

        for available_guest in available_data:
            only_names.append(available_guest["name"])
            available_names.append(available_guest["name"])
            available_names.append(available_guest["price"])
            names_and_values.append(available_names)
            available_names = []
        return names_and_values, only_names


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        # TODO слишком много лишних переменных создаётся для окна добавления пользователя
        self.view = app
        self.combobox = ttk.Combobox(self)
        self.left_button = ttk.Button(self)
        self.right_button = ttk.Button(self)
        self.info_label = ttk.Label(self)
        self.available_tobaccos = Main.find_data_from_db("tobaccos")[1]
        self.available_guests = Main.find_data_from_db("guests")[1]

    def add_guest(self):
        self.title("Добавление пользователя")
        self.geometry("200x150+400+300")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        window_description = ttk.Label(self, text="Введи имя гостя, чтобы\n"
                                                  "добавить его в список.")
        window_description.pack()
        new_guest_label = ttk.Label(self, text="Имя гостя: ")
        new_guest_label.place(x=60, y=60)
        guest_name = ttk.Entry(self)
        guest_name.place(x=35, y=80)

        self.right_button.config(text="Закрыть", command=lambda: self.destroy())
        self.right_button.place(x=115, y=120)
        self.left_button.config(text="Добавить", command=lambda: self.check_user_name(guest_name.get()))
        self.left_button.place(x=40, y=120)

    def add_tobacco(self):
        height = 200
        width = 200
        self.title("Добавление табака")
        self.geometry(str(width) + "x" + str(height) + "+400+300")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        window_description = ttk.Label(self, text="Введи название табака и его\n"
                                                  "стоимость, чтобы добавить табак\n"
                                                  "в список.")
        window_description.pack()
        new_tobacco_label = ttk.Label(self, text="Название табака:")
        new_tobacco_label.place(x=49, y=60)
        tobacco_name = ttk.Entry(self)
        tobacco_name.place(x=35, y=80)

        new_tobacco_price_label = ttk.Label(self, text="Стоимость табака:")
        new_tobacco_price_label.place(x=45, y=110)
        tobacco_price = ttk.Entry(self)
        tobacco_price.place(x=35, y=130)

        self.right_button.config(text="Закрыть", command=lambda: self.destroy())
        self.right_button.place(x=115, y=height - 30)
        self.left_button.config(text="Добавить", command=lambda: self.check_tobacco_name(tobacco_name.get(),
                                                                                         tobacco_price.get()))
        self.left_button.place(x=40, y=height - 30)

    def check_user_name(self, guest_name):
        if guest_name in self.available_guests:
            self.window(text="гость с таким именем уже существует", color="red", previous_window="add_guest")
            self.destroy()
        else:
            try:
                # TODO не нужно постоянно уничтожать целое окно, надо менять значения переменных в конфигах
                self.destroy()
                if guest_name == "":
                    raise TypeError
                elif re.match(r"^[a-zA-Zа-яА-Я0-9]+$", guest_name) is None:
                    raise TypeError
                hookah_users_db.insert_one({"name": guest_name, "price": 0.00})
                Main.update_table(app, "guests")
                self.window("пользователь\n успешно добавлен", "black", previous_window="add_guest")
            except TypeError:
                self.window(text="это не \nподходящее имя", color="red", previous_window="add_guest")

    def check_tobacco_name(self, tobacco_name, price):
        if tobacco_name in self.available_tobaccos:
            self.window(text="Табак с таким названием уже существует", color="red", previous_window="add_guest")
            self.destroy()
        else:
            try:
                # TODO не нужно постоянно уничтожать целое окно, надо менять значения переменных в конфигах
                self.destroy()
                price = int(price)
                if price < 0:
                    raise ValueError
                if tobacco_name == "":
                    raise TypeError
                elif re.match(r"^[a-zA-Zа-яА-Я0-9]+$", tobacco_name) is None:
                    raise TypeError
                tobaccos_db.insert_one({"name": tobacco_name, "price": price})
                Main.update_table(app, "tobaccos")
                self.window("табак\n успешно добавлен", "black", previous_window="add_tobacco")
            except TypeError:
                self.window(text="это не \nподходящее название", color="red", previous_window="add_guest")
            except ValueError:
                self.window(text="это не \nподходящая цена\nдля табака", color="red", previous_window="add_tobacco")

    def add_hype(self, guests):
        window_height_coefficient = len(self.available_tobaccos) + 1 \
            if len(self.available_tobaccos) + 1 >= len(self.available_guests) else len(self.available_guests)
        self.height_inc = 30
        self.window_height = 60 + self.height_inc * window_height_coefficient
        self.title("Добавление тусы")
        self.geometry("200x" + str(self.window_height) + "+400+300")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        # переменные для окна тус
        self.coals_label = ttk.Label(self)
        self.events = []
        Child.add_hype_guests(self, guests)

    def add_hype_guests(self, guests, smoked_guests=None, labels=None, smoked_tobaccos=None):

        def b1(event):
            if self.events:
                if str(event.widget) in self.events:
                    index = self.events.index(str(event.widget))
                    self.events.pop(index)
                    if not self.events:
                        self.left_button.config(state=tk.DISABLED)
                else:
                    self.events.append(str(event.widget))
                    self.left_button.config(state=tk.NORMAL)
            else:
                self.events.append(str(event.widget))
                self.left_button.config(state=tk.NORMAL)

        # стираем лейблы, переданные в этот метод
        if labels is not None:
            for label in labels:
                label[0].destroy()
                label[1].destroy()
                label[3].destroy()
            # b1("create")
            self.coals_label.config(text="")
            # TODO неправильно убирать комбобокс за пределы экрана, надо его просто скрывать
            self.combobox.place(x=-2000, y=0)

        self.info_label.config(text="Выберите, кто из гостей курил: ")
        self.info_label.place(x=5, y=5)
        label_place_y = 0
        smoked_guests_check = []
        labels = []

        for guest in guests:
            label_place_y += self.height_inc
            guest_name_label = ttk.Label(self)
            guest_name_label.config(text=guest + ": ")
            guest_name_label.place(x=5, y=label_place_y)
            check_var = tk.BooleanVar()
            if smoked_guests is not None:
                if guest in smoked_guests:
                    check_var.set(value=1)
            smoked_guests_check.append([guest, check_var])
            tick_label = ttk.Checkbutton(self, variable=check_var)
            tick_label.place(x=160, y=label_place_y)
            labels.append([guest_name_label, tick_label, check_var])
            tick_label.bind('<Button-1>', b1)

        def smoked_guests_checker():
            smokd_guests = []
            tick = 1
            for iterate in range(len(smoked_guests_check)):
                if smoked_guests_check[iterate][1].get() is True:
                    smokd_guests.append(smoked_guests_check[iterate][0])
            if smokd_guests:
                for item in labels:
                    item[tick].destroy()
                Child.add_hype_tobaccos(self, guests, labels, smokd_guests, smoked_tobaccos)
            else:
                self.window(text="Нельзя выбирать 0 гостей", color="red")

        self.right_button.config(text="Закрыть", command=lambda: self.destroy())
        self.right_button.place(x=115, y=self.window_height - 30)
        self.left_button.config(text="Далее",
                                command=functools.partial(smoked_guests_checker))
                                #command=lambda: smoked_guests_checker())
        self.left_button.place(x=40, y=self.window_height - 30)
        # TODO лучше не уничтожать чекбаттоны, чем использовать говнокод снизу
        if self.events:
            self.left_button.config(state=tk.NORMAL)
            old_events_len = len(self.events)
            for i in range(old_events_len):
                new_event = self.events[i].partition("n")
                eventr = new_event[0] + new_event[1] + str(int(new_event[2]) + len(smoked_guests_check))
                self.events.append(eventr)
            for i in range(old_events_len):
                self.events.pop(i - i)
        else:
            self.left_button.config(state=tk.DISABLED)

    def add_hype_tobaccos(self, guests, window_labels, smoked_guests, smoked_tobaccos=None):
        self.info_label.config(text="Укажите табаки и кол-во углей:")
        smoked_tobaccos_check = []
        percents = [x for x in range(101) if x % 5 == 0]
        label_place_y = self.height_inc * len(guests) if len(guests) < len(self.available_tobaccos) \
            else self.height_inc * len(self.available_tobaccos)
        if len(self.available_tobaccos) < len(guests):
            redundant_names = 0
            tobacco_labels_count = len(self.available_tobaccos)
            for label in window_labels[tobacco_labels_count:]:
                label[redundant_names].destroy()
                window_labels.pop(tobacco_labels_count)

        elif len(self.available_tobaccos) > len(guests):
            tobacco_labels_count = len(guests)
            for i in range(len(self.available_tobaccos[tobacco_labels_count:])):
                tobacco_name_label = ttk.Label(self)
                tobacco_name_label.config(text=self.available_tobaccos[tobacco_labels_count + i] + ":")
                tobacco_name_label.place(x=5, y=label_place_y + self.height_inc * (i + 1))
        for i in range(len(window_labels)):
            window_labels[i][0].config(text=self.available_tobaccos[i] + " (в % от чаши):")
            combobox = ttk.Combobox(self, values=percents, width=3)
            if smoked_tobaccos:
                for smoked_tobacco in smoked_tobaccos:
                    if self.available_tobaccos[i] in smoked_tobacco:
                        index = percents.index(int(smoked_tobacco[1]))
                        combobox.current(index)
                        break
                    else:
                        combobox.current(0)
            else:
                combobox.current(0)
            combobox.place(x=155, y=label_place_y - self.height_inc * (len(window_labels) - i - 1))
            window_labels[i].append(combobox)
            smoked_tobaccos_check.append([self.available_tobaccos[i], combobox])

        def btn_press(btn=None):
            smokd_tobacco = []
            total_percent = 0

            for x in range(len(smoked_tobaccos_check)):
                total_percent += int(smoked_tobaccos_check[x][1].get())
                if int(smoked_tobaccos_check[x][1].get()) > 0:
                    smokd_tobacco.append([smoked_tobaccos_check[x][0], smoked_tobaccos_check[x][1].get()])
            if btn == "Добавить":
                if total_percent > 100 or total_percent <= 0:
                    self.window(text="Общий процент табака в чаше\nне должен превышать 100%", color="red")
                else:
                    self.calculation(smokd_tobacco, self.combobox.get(), smoked_guests)
            elif btn == "Назад":
                self.add_hype_guests(guests, smoked_guests, window_labels, smokd_tobacco)

        self.coals_label.config(text="Количество углей:")
        self.coals_label.place(x=5, y=label_place_y + self.height_inc)
        self.combobox.config(values=[u"3", u"4", "5"], width=3)
        self.combobox.current(0)
        self.combobox.place(x=155, y=label_place_y + self.height_inc)
        self.right_button.config(text="Назад",
                                 command = functools.partial(btn_press, "Назад"))
                                 #command=lambda: btn_press("Назад"))
        self.left_button.config(text="Добавить", command=lambda: btn_press("Добавить"))

    @staticmethod
    def window(text, color, previous_window=None):
        window = tk.Toplevel()
        window.title("Операция выполнена")
        window.geometry("300x100+400+300")
        window.resizable(False, False)
        window.grab_set()
        window.focus_set()
        msg = tk.Label(window, text=text.upper(), fg=color)
        msg.pack(side=tk.TOP)

        def btn_press():
            window.destroy()
            # TODO поставить проверку на опечатку в названии предыдущего окна
            if previous_window == "add_guest":
                Child().add_guest()
            elif previous_window == "add_tobacco":
                Child().add_tobacco()

        btn_ok = ttk.Button(window, text="Ок", command=lambda: btn_press())
        btn_ok.place(x=110, y=70)

    def calculation(self, used_tobaccos, coals, smoked_guests):
        bowl_mass = 15
        bowl_price = 0.0
        pack_mass = 50
        tobacco_names_and_prices = Main.find_data_from_db("tobaccos")[0]

        for used_tobacco in used_tobaccos:
            for tobacco_name_and_price in tobacco_names_and_prices:
                if used_tobacco[0] in tobacco_name_and_price:
                    used_tobacco.append(tobacco_name_and_price[1])
        for i in range(len(used_tobaccos)):
            bowl_price += (float(used_tobaccos[i][2]) * (float(used_tobaccos[i][1]) / 100.0) * bowl_mass) / pack_mass

        personal_price = (bowl_price + int(coals) * 4.17) / len(smoked_guests)
        available_guests = hookah_users_db.find({})
        for guest in available_guests:
            if guest["name"] in smoked_guests:
                print(guest)
                new_price = guest["price"] + personal_price
                print(new_price)
                update_user_price = {"name": guest["name"], "price": new_price}
                print(update_user_price)
                hookah_users_db.find_one_and_replace({"name": guest["name"]}, update_user_price)
        self.destroy()
        Main.update_table(app, updated_table="guests")


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
    root.geometry("650x600+300+200")
    root.resizable(False, True)
    root.mainloop()
