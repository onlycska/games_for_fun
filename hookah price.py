#!/usr/bin/env python3

import re
import datetime
import base64
from pymongo import MongoClient

DEFAULT_BOWL_MASS = 15.0  # how much tobacco at once can I use with my bowl
PACK_MASS = 50.0  # standard mass of tobacco pack




def main():
    """
    the instruction creates and updates tables in database
    :return: nothing
    """
    connect = base64.standard_b64decode("bW9uZ29kYjovL2hvb2thaDoxMzAzOTdvbGVnQGRz"
                                        "MjQ3MjIzLm1sYWIuY29tOjQ3MjIzL29ubHljc2th")
    connect = connect.decode('utf-8')
    client = MongoClient(connect)
    db = client["onlycska"]
    events = db["events"]
    tobaccos = db["tobaccos"]
    hookah_users = db["guests"]

    guests = my_guests(hookah_users)
    used_tobaccos = smoked_tobacco(tobaccos)
    coals = int(used_coals())
    price = price_counter(len(guests), used_tobaccos, coals)
    event = {"date": str(datetime.date.today()),
             "guests": guests, "smoked_tobaccos": used_tobaccos, "coals": coals, "personal_price": price}
    events.insert_one(event)
    print("Event created:\n", event)

    counter = 0
    while True:
        ex_guests = hookah_users.find({})
        count = hookah_users.count_documents({})
        if count > 0:
            for ex_guest in ex_guests:
                if guests[counter] == ex_guest["name"]:
                    guests.pop(counter)
                    counter -= 1
                    new_price = ex_guest["price"] + price
                    update_user_price = {"name": ex_guest["name"], "price": new_price}
                    hookah_users.find_one_and_replace({"name": ex_guest["name"]}, update_user_price)
                    break
            else:
                hookah_users.insert_one({"name": guests[counter], "price": price})

        else:
            hookah_users.insert_one({"name": guests[counter], "price": price})
        counter += 1
        if counter >= len(guests):
            break


def my_guests(ex_guests):
    """
    This instruction identifies guests who used tobacco and hookah coal that I bought.
    hookah_users - guests who smoked hookah
    """
    # hookah_users = []
    # guest = input("Oleg and Tanya smoked hookah, [] - yes, [...] - no: ")
    #
    # if guest == "":
    #     hookah_users.extend(("Oleg", "Tanya"))
    #
    # while True:
    #     guest = input("Enter name of guest (use literals), [] - over: ")
    #     if guest == "":
    #         if len(hookah_users) == 0:
    #             print("\nIt has to be one guest at least\n")
    #         else:
    #             print("\nName entry is over\n")
    #             break
    #     else:
    #         try:
    #             match = re.match(r"^[a-zA-Zа-яА-Я]+$", guest)[0]
    #         except TypeError:
    #             print("\nIt's not a name\n".upper())
    #         else:
    #             print(match)
    #             hookah_users.append(match)
    hookah_users = []
    available_guests_names = []

    count = ex_guests.count_documents({})
    available_guests = ex_guests.find({})

    for available_guest in available_guests:
        available_guests_names.append(available_guest["name"])

    if count > 0:
        print("There is {} guests already in database: {}".format(count,
                                                                  "%s" % ", ".join(map(str, available_guests_names))))
    else:
        print("There is no tobaccos")

    # Update tobaccos collection if needed
    while True:

        should_update_collection = input("Do you want to enter new guest? [y] - Yes, other - No: ")

        if should_update_collection.lower() == "y" or should_update_collection.lower() == "н":
            while True:
                try:
                    new_tobacco = input("Enter tobacco name: ")
                    if new_tobacco == "":
                        raise TypeError
                    re.match(r"^[a-zA-Zа-яА-Я]+$", new_tobacco)
                except TypeError:
                    print("\nThis is not a name of guest\n".upper())
                    continue
                # try:
                #     tobacco_price = int(input("Enter {} price: ".format(new_tobacco)))
                # except ValueError:
                #     print("\nThis is not a number\n".upper())
                # else:
                #     ex_guests.insert_one({"name": new_tobacco, "price": tobacco_price})
        else:
            if count != 0:
                break
            elif count == 0:
                print("\nit cannot be 0 guests in database\n".upper())
                continue

    for i in range(count):
        guest_name = input("Did {} smoked the tobacco ? [] - yes, [...] - no: ".format(available_guests_names[i]))
        if guest_name == "":
            hookah_users.append(available_guests_names[i])
        else:
            continue
    print(hookah_users)
    raise SystemExit()
    return hookah_users


def smoked_tobacco(available_tobaccos_collection):
    """
    The instruction defines which tobaccos and in which ratio were use.
    used_tobaccos - used tobaccos
    available_tobaccos_names - tobaccos that currently exists in database
    """
    used_tobaccos = []
    available_tobaccos_names = []

    count = available_tobaccos_collection.count_documents({})
    available_tobaccos = available_tobaccos_collection.find({})

    for available_tobacco in available_tobaccos:
        available_tobaccos_names.append(available_tobacco["name"])

    if count > 0:
        print("There is {} available tobaccos: {}".format(count, "%s" % ", ".join(map(str, available_tobaccos_names))))
    else:
        print("There is no tobaccos")

    # Update tobaccos collection if needed
    while True:

        should_update_collection = input("Do you want to enter new tobacco? [y] - Yes, other - No: ")

        if should_update_collection.lower() == "y" or should_update_collection.lower() == "н":
            while True:
                try:
                    new_tobacco = input("Enter tobacco name: ")
                    if new_tobacco == "":
                        raise TypeError
                    re.match(r"^[a-zA-Zа-яА-Я]+$", new_tobacco)
                except TypeError:
                    print("This is not a name of tobacco")
                    continue
                try:
                    tobacco_price = int(input("Enter {} price: ".format(new_tobacco)))
                except ValueError:
                    print("\nThis is not a number\n".upper())
                else:
                    available_tobaccos_collection.insert_one({"name": new_tobacco, "price": tobacco_price})
        else:
            if count != 0:
                break
            elif count == 0:
                print("it cannot be 0 tobaccos in database".upper())
                continue

    for i in range(count):
        used_tobacco_name = input("Did you smoke the tobacco {}? [] - yes, [...] - no: ".format
                                  (available_tobaccos_names[i]))
        if used_tobacco_name == "":
            used_tobaccos.append([available_tobaccos_collection.find({"name": available_tobaccos_names[i]})[0]])
        else:
            continue

    counter = 0
    portion = 0

    while portion != 100:

        smoke = input("Enter how much {} was used (in %, {}% left), [over] - over: ".format
                      (used_tobaccos[counter][0]["name"], 100 - portion))
        if smoke == "over" and portion == 0:
            print("\nYou can't add 0 smoked tobaccos\n".upper())
            continue
        elif smoke == "over" and portion != 0:
            break
        try:
            portion += int(smoke)
            if len(used_tobaccos[counter]) == 1:
                used_tobaccos[counter].append(smoke)
            else:
                refactorer = int(smoke) + used_tobaccos[counter][1]
                used_tobaccos[counter].pop()
                used_tobaccos.append(refactorer)
        except ValueError:
            print("\nThis is not a number\n".upper())

        if portion == 0 and smoke == "":
            print("\nYou can't add 0 smoked tobaccos\n".upper())

        if portion > 100:
            portion -= int(smoke)
            print("\nYou've input number with which sum of used tobacco (in %) overvalue 100%\n".upper())
        if counter >= len(used_tobaccos) - 1:
            counter = 0
        else:
            counter += 1
    # print(used_tobaccos)
    return used_tobaccos


def used_coals():
    """
    the instruction defines:
    :return: how much coals were used
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

    return coals


def price_counter(guests, used_tobaccos, coals):
    """
    the instruction defines price for hype at one person who smoked hookah
    :param guests: how much guests were in the hype
    :param used_tobaccos: which tobaccos were used on hype
    :param coals: how much coals were used on hype
    :return: price for every person who smoked hookah
    """
    bowl_mass = DEFAULT_BOWL_MASS
    bowl_price = 0.0
    pack_mass = PACK_MASS

    for i in range(len(used_tobaccos)):
        bowl_price += (float(used_tobaccos[i][0]["price"]) *
                       (float(used_tobaccos[i][1]) / 100.0) * bowl_mass) / \
                      pack_mass

    personal_price = round((bowl_price + coals * 4.17) / guests, 3)

    return personal_price


main()
