#!/usr/bin/env python3

import os
import json


def main():
    """


    """
    file = create_path()
    hookah_users = my_guests()
    tobaccos = smoked_tobacco()
    prices = price_counter(tobaccos, len(hookah_users))


def my_guests():
    """
    This instruction identifies guests who used tobacco and hookah coal that I bought.
    hookah_users - guests who smoked hookah
    """
    hookah_users = []
    guest = input("Oleg and Tanya smoked hookah, [] - yes, [...] - no:")
    if guest == "":
        hookah_users.append("Oleg")
        hookah_users.append("Tanya")
    while True:
        guest = input("Enter name of guest (use literals), [] - over: ")
        if guest == "" and hookah_users == []:
            print("\nIt has to be one guest at least\n")
        elif guest == "" and hookah_users != []:
            print("\nName entry is over\n")
            break
        else:
            try:
                guest = int(guest)
                print("\nIt's not a name\n".upper())
            except ValueError:
                hookah_users.append(guest)
    return hookah_users


def create_path():
    filepath = os.path.join(r'C:\Users\Admin\Desktop\мои работы\прожки', 'hookah price.txt')
    if not os.path.exists(r'C:\Users\Admin\Desktop\мои работы\прожки'):
        os.makedirs(r'C:\Users\Admin\Desktop\мои работы\прожки')
    return filepath


def smoked_tobacco():
    """
    The instruction defines which tobaccos and in which ratio were use.
    used_tobaccos[x][0] - tobacco name
    used_tobaccos[x][1] - percent of used tobacco in ratio to all used tobacco
    """
    # parser = open(file, "w+")
    tobaccos = {1: "adalya", 2: "dali", 3: "horse"}
    tobacco = 0
    used_tobaccos = []
    while True:
        smoke = input("Enter used tobacco (where [1] = {}, [2] = {}, [3] = {}, [] - over): ".format(tobaccos[1],
                                                                                                    tobaccos[2],
                                                                                                    tobaccos[3]))
        # if type(smoke) == int:
        if len(used_tobaccos) == 0 and smoke == "":
            print("\nYou can't add 0 smoked tobaccos\n".upper())
        elif len(used_tobaccos) != 0 and smoke == "":
            break
        else:
            try:
                smoke = int(smoke)
                if len(used_tobaccos) == 0:
                    used_tobaccos.append([tobaccos[smoke]])
                else:
                    for i in range(len(used_tobaccos)):
                        if used_tobaccos[i][0] == tobaccos[smoke]:
                            print("You've input already this tobacco")
                            break
                        else:
                            continue
                    else:
                        used_tobaccos.append([tobaccos[smoke]])
            except ValueError:
                print("\nThis is not a number\n".upper())
            except KeyError:
                print("\nThere is no tobacco with this number\n".upper())
    counter = 0
    while tobacco != 100:
        if counter == len(used_tobaccos):
            counter = 0
        smoke = input("Enter how much {} was used (in %, {}% left): ".format(used_tobaccos[counter][0].upper(),
                                                                             100-tobacco))
        try:
            tobacco += int(smoke)
            used_tobaccos[counter].append(smoke)
        except ValueError:
            print("\nThis is not a number\n".upper())
        if tobacco == 0 and smoke == "":
            print("\nYou can't add 0 smoked tobaccos\n".upper())
        if tobacco > 100:
            tobacco -= int(smoke)
            print("\nYou've input number with which sum of used tobacco (in %) overvalue 100%\n".upper())
        counter += 1
    return used_tobaccos


def price_counter(tobaccos, hookah_users):
    """

    :param tobaccos: the same as used_tobacco in previous instruction
    :param hookah_users: how much guests smoked hookah
    :return:
    """
    while True:
        coals = input("How much coals were used, 3 is default, [] - over:")
        if coals != "":
            try:
                coals = int(coals)
                break
            except ValueError:
                print("\nThis is not a number\n".upper())
        else:
            coals = 3
            break
    bowl_mass = 30
    tobacco_dict = dict(adalya=120, dali=276, horse=184)
    bowl_price = 0
    pack_mass = 50
    for i in range(len(tobaccos)):
        # print(tobacco_dict[tobaccos[i][0]])
        bowl_price += (tobacco_dict[tobaccos[i][0]] * (int(tobaccos[i][1]) / 100) * bowl_mass) / pack_mass
    personal_price = round((bowl_price + coals*4.17)/hookah_users, 3)
    print(personal_price)


main()
