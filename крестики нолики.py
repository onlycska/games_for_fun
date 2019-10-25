import tkinter as tk
from tkinter import ttk
import math


class Calculations:
    def __init__(self, table_size):
        super().__init__()
        self.table_size = table_size

    @staticmethod
    def win_checker(clicked_buttons, table_size, all_butons=[]):
        print("win_checker started")
        print(clicked_buttons)
        win = False
        # проверка комбинаций нажатых ячеек, необходимых для победы - диагональные ряды
        if set([table_size*k+k+1 for k in range(0, table_size)]).issubset(clicked_buttons):
            win = True
        elif set([table_size*k-k+1 for k in range(1, table_size+1)]).issubset(clicked_buttons):
            win = True
        for i in range(table_size):
            # проверка комбинаций нажатых ячеек, необходимых для победы - горизонтальные и вертикальные ряды
            if set(range(table_size*i+1, table_size*(i+1)+1)).issubset(clicked_buttons):
                win = True
                break
            elif set([table_size*k+i+1 for k in range(table_size)]).issubset(clicked_buttons):
                win = True
                break
        if win:
            print("winner defined")
            global first_player_move
            winner_number = "First player" if first_player_move else "Second player"
            TableForGame.another_game_start(app, winner_number)
        elif len(clicked_buttons) == math.ceil(table_size**2/2):
            # для определения ничьей нужно убедиться, что все клетки были выбраны
            draw_define = 0
            for button in all_butons:
                if button["text"]:
                    draw_define += 1
                    print(draw_define)
            if draw_define == table_size**2:
                print("draw defined")
                TableForGame.another_game_start(app, "")
        else:
            print("winner not defined")

    @staticmethod
    def change_size(old_size, new_size):
        if str(old_size) in new_size:
            pass
        else:
            global app
            global main_window
            app.destroy()
            main_window.destroy()
            main_window = tk.Tk()
            app = TableForGame(main_window, int(new_size[0]))
            main_window.mainloop()

    @staticmethod
    def prepare_for_win_checker(list_of_clicked_buttons, button_number, table_size, buttons):
        global first_player_move
        list_of_clicked_buttons.append(button_number)
        if len(list_of_clicked_buttons) > table_size - 1:
            Calculations.win_checker(list_of_clicked_buttons, table_size, buttons)
        first_player_move = not first_player_move


class TableForGame(tk.Frame):
    def __init__(self, window_with_table, size):
        super().__init__(window_with_table)
        window_with_table.title("Крестики-нолики")
        x_window_size = str(size*90)
        y_window_size = str(size*90 + 60)
        window_with_table.geometry(x_window_size + "x" + y_window_size)
        window_with_table.resizable(False, False)
        self.who_move_label = ttk.Label(text="First player move")
        self.buttons = []
        self.score_label = tk.Label()
        self.table_size = size
        self.buttons_creation(first_fight=True)

    def buttons_creation(self, first_fight=False, repeat_fight=False):
        if first_fight:
            self.who_move_label.grid(row=1, column=0, columnspan=self.table_size)
            for i in range(self.table_size**2):
                self.buttons.append(tk.Button(font='Times 20 bold', bg='white', fg='black', height=2, width=5))

            row = 2
            column = 0
            index = 1
            for button in self.buttons:
                button.grid(row=row, column=column)
                button.config(command=lambda current_button=button: TableForGame.change_button_text(app,
                                                                                                    current_button))
                column += 1
                if index % self.table_size == 0:
                    row += 1
                    column = 0
                index += 1
            self.score_label.grid(row=self.table_size + 2, column=0, columnspan=self.table_size)
            btn_clear_table = tk.Button(text="New game", command=lambda: self.new_game_from_button(),
                                        bg="#FFCFFF")
            btn_clear_table.grid(row=self.table_size + 3, column=0)
            change_table_size = ttk.Combobox(values=["3x3", "4x4"], width=8)
            change_table_size.current(0)
            change_table_size.grid(row=self.table_size+3, column=2)
            btn_change_table_size = tk.Button(text="Change size", bg="#FFCFFF",
                                              command=lambda: Calculations.change_size(self.table_size,
                                                                                       change_table_size.get()))
            btn_change_table_size.grid(row=self.table_size + 3, column=1)
        if repeat_fight:
            global crosses, nulls
            crosses = []
            nulls = []
            for button in self.buttons:
                button.config(text="")
        score_text_for_label = "First player {} : {} Second player".format(str(score["First player"]),
                                                                           str(score["Second player"]))
        self.score_label.config(text=score_text_for_label)

    def change_button_text(self, clicked_button):
        global first_player_move
        button_number = str(clicked_button).split("n")
        print(button_number)
        button_number = 1 if button_number[1] == "" else int(button_number[1])
        if clicked_button["text"] == "" and first_player_move is True:
            clicked_button.config(text="✖")
            Calculations.prepare_for_win_checker(crosses, button_number, self.table_size, self.buttons)
            self.who_move_label.config(text="Second player move")
        elif clicked_button["text"] == "" and first_player_move is False:
            clicked_button.config(text="⚪")
            Calculations.prepare_for_win_checker(nulls, button_number, self.table_size, self.buttons)
            self.who_move_label.config(text="First player move")

    def another_game_start(self, player_won):
        # начало очередной игры, обновление счёта
        self.destroy()
        if player_won:
            new_score = score[player_won] + 1
            score.update({player_won: new_score})
        TableForGame.buttons_creation(app, repeat_fight=True)

    def new_game_from_button(self):
        # для новой игры обнуляется счёт, ход отдается первому игроку
        global first_player_move
        score.update({"First player": 0, "Second player": 0})
        first_player_move = True
        self.who_move_label.config(text="First player move")
        self.buttons_creation(repeat_fight=True)


if __name__ == "__main__":
    first_player_move = True
    crosses = []
    nulls = []
    score = dict([("First player", 0), ("Second player", 0)])
    main_window = tk.Tk()
    app = TableForGame(main_window, 3)
    main_window.mainloop()
