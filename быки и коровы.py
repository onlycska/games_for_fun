import random
print("""Игрок делает первую попытку отгадать число.
Попытка — это 4-значное число, сообщаемое компьютеру.
Компьютер сообщает в ответ, сколько цифр угадано вплоть до позиции в тайном числе (то есть количество быков) 
и сколько угадано без совпадения с их позициями в тайном числе(то есть количество коров).
Например:
Задумано тайное число «3211». Попытка: «2310».
Результат: две «коровы»(две цифры: «2» и «3» — угаданы на неверных позициях) и один «бык» (одна цифра «1» угадана 
вплоть до позиции). Цифра "1" учитывается в этом случае только как "бык", несмотря на то, что она может быть ещё и
"коровой". Смысл в том, что цель игры угадать 4 "быков", поэтому они учитываются в первую очередь. Одна цифра в 
введённом числе не может быть одновременно и "быком" и "коровой" - это только запутает игрока.
Игрок вводит комбинации одну за другой, пока не отгадает всю последовательность.\n""")


def number_input():
    user_number = None  # input ("Введите четырёхзначное число: ")

    def input_number_checker(checked_number):
        if type(checked_number) is not int:
            print("Нужно вводить ЧИСЛО.")
            return False
        elif checked_number not in range(1000, 10000):
            print("Число должно быть ЧЕТЫРЁХзначным.")
            return False
        elif checked_number in range(1000, 10000):
            return True

    while True:
        if user_number is None:
            user_number = input("Введите четырёхзначное число: ")
        try:
            user_number = int(user_number)
        except ValueError:
            pass
        if input_number_checker(user_number):
            return int(user_number)
        user_number = None


number = str(random.randrange(1000, 9999))
moves = ""
while True:
    choice = input("Выберите уровень сложности [0 - easy, 1 - medium, 2 - hard, 3 - fucking hard]: ")
    if choice == "0":
        moves = 20
    elif choice == "1":
        moves = 15
    elif choice == "2":
        moves = 10
    elif choice == "3":
        moves = 7
    else:
        continue
    break

for move in range(moves):
    not_used_move = moves - move
    if not_used_move > 4:
        print("На игру дано {} ходов. \nОсталось {} ходов".format(moves, moves - move))
    elif 4 >= not_used_move > 1:
        print("На игру дано {} ходов. \nОсталось {} хода".format(moves, moves - move))
    else:
        print("На игру дано {} ходов. \nОстался 1 ход".format(moves))
    user_number = number_input()
    user_number = str(user_number)
    cow = 0
    bull = 0
    trial_number = number
    if user_number == number:
        bull = 4
    else:
        for i in range(len(number)):
            if trial_number[i] == user_number[i]:
                bull += 1
                trial_number = trial_number[0:i] + "x" + trial_number[i+1:]
                user_number = user_number[0:i] + "y" + user_number[i+1:]
        for i in range(len(number)):
            if trial_number[i] != "x":
                for k in range(len(number)):
                    if user_number[k] == trial_number[i]:
                        cow += 1
                        trial_number = trial_number[0:i] + "x" + trial_number[i + 1:]
                        user_number = user_number[0:k] + "y" + user_number[k + 1:]
    print("Быки = ", bull, "Коровы = ", cow)
    if bull == 4:
        print("Число угадано. Ты молодец.\n")
        break
else:
    print("\nПОТРАЧЕНО\nОтвет: ", number)
