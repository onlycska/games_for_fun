import tkinter as tk
from tkinter import ttk


class Calculations:
    def __init__(self, table_size):
        super().__init__()
        self.table_size = table_size

    @staticmethod
    def win_checker(clicked_buttons, table_size=3):
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
            global button_click
            winner_number = "First player" if button_click else "Second player"
            TableForGame.repeat_game_start(app, winner_number)
        elif len(clicked_buttons) == 5:
            print("draw defined")
            TableForGame.repeat_game_start(app, "")
        else:
            print("winner not defined")


class TableForGame(tk.Frame):
    def __init__(self, window_with_table):
        super().__init__(window_with_table)
        window_with_table.title("Крестики-нолики")
        window_with_table.geometry("270x450")
        window_with_table.resizable(False, False)
        self.who_move_label = ttk.Label(text="First player move")
        self.buttons = []
        self.score_label = tk.Label()
        self.table_size = 3
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
            btn_clear_table = tk.Button(text="Очистить поле", command=lambda: self.buttons_creation(repeat_fight=True),
                                        bg="#FFCFFF")
            btn_clear_table.grid(row=self.table_size + 3, column=0)
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
        global button_click
        button_number = str(clicked_button)[-1]
        button_number = 1 if button_number == "n" else int(button_number)
        if clicked_button["text"] == "" and button_click is True:
            clicked_button.config(text="✖")
            crosses.append(button_number)
            if len(crosses) > 2:
                Calculations.win_checker(crosses)
            button_click = False
            self.who_move_label.config(text="Second player move")
        elif clicked_button["text"] == "" and button_click is False:
            clicked_button.config(text="⚪")
            nulls.append(button_number)
            if len(nulls) > 2:
                Calculations.win_checker(nulls)
            button_click = True
            self.who_move_label.config(text="First player move")

    def repeat_game_start(self, player_won):
        self.destroy()
        if player_won:
            new_score = score[player_won] + 1
            score.update({player_won: new_score})
        TableForGame.buttons_creation(app, repeat_fight=True)


if __name__ == "__main__":
    button_click = True
    crosses = []
    nulls = []
    score = dict([("First player", 0), ("Second player", 0)])
    main_window = tk.Tk()
    app = TableForGame(main_window)
    main_window.mainloop()
