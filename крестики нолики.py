import tkinter as tk
from tkinter import ttk

button_click = True
main_window = tk.Tk()
main_window.title("Крестики-нолики")
main_window.geometry("270x255")
buttons = []
crosses = []
nulls = []


def win_checker(clicked_buttons):
    win = False
    if 1 in clicked_buttons and 2 in clicked_buttons and 3 in clicked_buttons:
        win = True
    elif 4 in clicked_buttons and 5 in clicked_buttons and 6 in clicked_buttons:
        win = True
    elif 7 in clicked_buttons and 8 in clicked_buttons and 9 in clicked_buttons:
        win = True
    elif 1 in clicked_buttons and 4 in clicked_buttons and 7 in clicked_buttons:
        win = True
    elif 2 in clicked_buttons and 5 in clicked_buttons and 8 in clicked_buttons:
        win = True
    elif 3 in clicked_buttons and 6 in clicked_buttons and 9 in clicked_buttons:
        win = True
    elif 1 in clicked_buttons and 5 in clicked_buttons and 9 in clicked_buttons:
        win = True
    elif 3 in clicked_buttons and 5 in clicked_buttons and 7 in clicked_buttons:
        win = True

    if win:
        global button_click
        message = "First player won" if button_click else "Second player won"
        info_window = tk.Toplevel()
        info_window.title("Определён победитель")
        info_window.geometry("200x150+100+100")
        info_window.resizable(False, False)
        info_window.grab_set()
        info_window.focus_set()
        window_description = ttk.Label(info_window, text=message)
        window_description.pack()


def change_button_text(clicked_button):
    global button_click
    clicked_button['state'] = "disabled"
    button_number = str(clicked_button)[-1]
    button_number = 1 if button_number == "n" else int(button_number)
    if clicked_button["text"] == "" and button_click is True:
        clicked_button.config(text="X")
        crosses.append(button_number)
        if len(crosses) > 2:
            win_checker(crosses)
        button_click = False
    elif clicked_button["text"] == "" and button_click is False:
        clicked_button.config(text="0")
        nulls.append(button_number)
        if len(nulls) > 2:
            win_checker(nulls)
        button_click = True


for i in range(9):
    buttons.append(tk.Button(font='Times 20 bold', bg='white', fg='black', height=2, width=5))

row = 1
column = 0
index = 1
for button in buttons:
    button.grid(row=row, column=column)
    button.config(command=lambda current_button=button: change_button_text(current_button))
    column += 1
    if index % 3 == 0:
        row += 1
        column = 0
    index += 1
main_window.mainloop()
