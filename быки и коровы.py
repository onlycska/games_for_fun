import random
print("""Игрок делает первую попытку отгадать число.
Попытка — это 4-значное число с неповторяющимися цифрами, сообщаемое компьютеру.
Компьютер сообщает в ответ, сколько цифр угадано без совпадения с их позициями в тайном числе(то есть количество коров)
и сколько угадано вплоть до позиции в тайном числе (то есть количество быков).
Например:
Задумано тайное число «3219».
Попытка: «2310».
Результат: две «коровы»(две цифры: «2» и «3» — угаданы на неверных позициях) и один «бык» (одна цифра «1» угадана 
вплоть до позиции).
Игрок вводит комбинации одну за другой, пока не отгадает всю последовательность.\n""")


number = random.randrange(1000, 9999, 1)


def number_input():
    number_user = None  # input ("Введите четырёхзначное число: ")
    while True:
        if number_user is None:
            number_user = input("Введите четырёхзначное число: ")
        try:
            number_user = int(number_user)
        except:
            None
        if type(number_user) is int and number_user not in range(1000, 10000):
            number_user = input("Введите ЧЕТЫРЁХзначное число: ")
        elif type(number_user) is not int:
            number_user = input("Введите четырёхзначное ЧИСЛО: ")
        elif number_user in range(1000, 10000):
            break
    return int(number_user)


for move in range(0, 10):
    if move != 8:
        print("На игру дано 10 ходов. \nЭто {} ход. \nОсталось {} ходов".format(move + 1, 9 - move))
    else:
        print("На игру дано 10 ходов. \nЭто 9 ход. \nОстался 1 ход")
    usernumber = number_input()
    number = str(number)
    usernumber = str(usernumber)
    cow = 0
    bull = 0
    for i in range(len(number)):
        n = 0
        trial_number = usernumber
        for n in range(len(usernumber)):
            if trial_number[n] == number[i] and i == n:
                bull += 1
                if n != 3 and n != 0:
                    trial_number = trial_number[:n] + "." + trial_number[n + 1:]
                    break
                elif n == 0:
                    trial_number = "." + trial_number[n + 1:]
                    break
                elif n == 3:
                    trial_number = trial_number[:n] + "."
                    break
            if trial_number[n] == number[i] and not i == n:
                cow += 1
                if n != 3 and n != 0:
                    trial_number = trial_number[:n] + "." + trial_number[n + 1:]
                    break
                elif n == 0:
                    trial_number = "." + trial_number[n + 1:]
                    break
                elif n == 3:
                    trial_number = trial_number[:n] + "."
                    break
            else:
                continue
    print("Быки = ", bull, "Коровы = ", cow)
    if bull == 4:
        break
else:
    print("\nПОТРАЧЕНО")
