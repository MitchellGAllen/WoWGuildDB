#-------------------------------------------------------------------------------
# Name:        Strictly Business SQL API
# Purpose:     Strictly Business SQL API
#
# Author:      CreationCatalyst
#
# Created:     08/05/2019
# Copyright:   (c) CreationCatalyst 2019
#-------------------------------------------------------------------------------

import datetime
import getpass
import mysql.connector
from mysql.connector import errorcode

def main():

    control = 1
    #host = input("Enter Server IP: ")
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")

    try:
        cnx = mysql.connector.connect   (user=str(username), password=str(password),
                                         #host = '127.0.0.1',
                                         #host = host,
                                         host = '67.158.140.55',
                                         port = '3306',
                                         database='loot',
                                         connection_timeout = 600)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            #print("Something is wrong with your username or password")
            print(err)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)



    while control == 1:

        data_input = int(input("""Enter Choice
1:  Add Item
2:  Record Item to Player
3:  Add Player
4:  Show Items of Player
5:  Show Qty of Tier
6:  Show Drops of Item
7:  List Players
8:  List Players by class
9:  List Items
10: Show Drops on Date
0: Quit: """))
        print("")

        if data_input == 1:
            item(cnx)

        elif data_input == 2:
            item_dist(cnx)

        elif data_input == 3:
            player(cnx)

        elif data_input == 4:
            item_by_player(cnx)

        elif data_input == 5:
            tier_qty(cnx)

        elif data_input == 6:
            item_by_item(cnx)

        elif data_input == 7:
            list_player(cnx)

        elif data_input == 8:
            list_player_class(cnx)

        elif data_input == 9:
            item_by_dung(cnx)

        elif data_input==10:
            list_by_date(cnx)

        elif data_input == 0:
            control = 0
            cnx.close()
        else:
            print("Input Error")
            print("")


def list_by_date(cnx):

    date_in = input("Enter Date ex.'YYYY-MM-DD': ")

    cursor = cnx.cursor()

    query = ("""SELECT item_dist.p_name AS p_name, item.item_name AS item_name
                FROM item_dist, item
                WHERE item_dist.item_id = item.item_id
                AND date_recieved = %s""")

    cursor.execute(query, (date_in,))

    count = 0

    print("")
    for(p_name, item_name) in cursor:
        count+=1
        print(str(count) + " | {} | {}".format(p_name, item_name))
    print("")

    cursor.close()

def item_by_dung(cnx):

    dungeon_in = input("Enter Dungeon Name: ")

    cursor = cnx.cursor()

    query = ("""SELECT item_id, item_name
                FROM item
                WHERE dungeon = %s""")

    cursor.execute(query, (dungeon_in,))

    count = 0

    print("")
    for(item_id, item_name) in cursor:
        count+=1
        print(str(count) + " | {} | {}".format(item_id, item_name))
    print("")

    cursor.close()

def list_player_class(cnx):

    class_input = input("Enter Class Name: ")

    cursor = cnx.cursor()

    query = ("""SELECT player.p_name AS p_name, spec.spec_name AS spec_name
                FROM player, spec
                WHERE player.spec_id = spec.spec_id
                AND spec.class = %s""")


    cursor.execute(query, (class_input,))

    count = 0

    print("")
    for(p_name, spec_name) in cursor:
        count += 1
        print(str(count) + " | {} | {}".format(p_name, spec_name))
    print("")

    cursor.close()

def list_player(cnx):

    cursor = cnx.cursor()

    query = ("""SELECT player.p_name AS p_name, spec.spec_name AS spec_name
                FROM player, spec
                WHERE player.spec_id = spec.spec_id""")

    cursor.execute(query)

    count = 0

    print("")
    for(p_name, spec_name) in cursor:
        count += 1
        print(str(count) + " | {} | {}".format(p_name, spec_name))
    print("")

    cursor.close()

def item_by_item(cnx):

    item = input("Enter Item Name: ")

    cursor = cnx.cursor()

    get_id = ("""SELECT item_id AS item_id
             FROM item
             WHERE item_name = %s""")

    query = ("""SELECT DISTINCT date_recieved AS date_recieved, p_name AS p_name
                FROM item_dist
                WHERE item_id = %s
                ORDER BY date_recieved""")

    cursor.execute(get_id, (item,))

    item_id = cursor.fetchone()

    cursor.execute(query, (item_id[0],))

    count = 0

    print("")
    print("Drops for " + item)
    for(date_recieved, p_name) in cursor:
        count += 1
        print(str(count) + " | {} | {}".format(date_recieved, p_name))
    print("")

    cursor.close()

def tier_qty(cnx):

    name = input("Enter Player Name: ")

    cursor = cnx.cursor()

    query = ("""SELECT DISTINCT item.item_id AS item_id
            FROM item_dist, item
            WHERE item_dist.p_name = %s
            AND item.is_tier = %s
            AND item_dist.item_id = item.item_id""")

    cursor.execute(query, (name, 1.0))
    count = 0

    for (item_id) in cursor:
        count += 1

    print("")
    print(name + " has " + str(count) + " pieces of tier 1.0")


    cursor.execute(query, (name, 2.0))
    count = 0

    for (item_id) in cursor:
        count += 1

    print(name + " has " + str(count) + " pieces of tier 2.0")



    cursor.execute(query, (name, 2.5))
    count = 0

    for (item_id) in cursor:
        count += 1

    print(name + " has " + str(count) + " pieces of tier 2.5")



    cursor.execute(query, (name, 3.0))
    count = 0

    for (item_id) in cursor:
        count += 1

    print(name + " has " + str(count) + " pieces of tier 3")
    print("")

    cursor.close()

def item_by_player(cnx):

    name = input("Enter Player Name: ")
    cursor = cnx.cursor()

    query = ("""SELECT DISTINCT item_dist.date_recieved AS date_recieved, item.dungeon AS dungeon, item.item_name AS item_name
             FROM item_dist, item
             WHERE item_dist.p_name = %s
             AND item_dist.item_id = item.item_id
             ORDER BY item_dist.date_recieved""")

    cursor.execute(query, (name,))

    count = 0

    print("")
    for (date_recieved, dungeon, item_name) in cursor:
        count += 1
        print(str(count) + " | {} | {} | {}".format(date_recieved, dungeon, item_name))
    print("")

    cursor.close()

def player(cnx):

    cursor = cnx.cursor()
    add_item = ("INSERT INTO player(p_name, spec_id)"
                "VALUES(%s, %s)")

    control = int(input("Enter number of entries: "))

    for x in range(control):

        data_item = (input("Enter Player Name: "), input("Enter Spec ID: "))

        cursor.execute(add_item, data_item)
        cnx.commit()

    cursor.close()

def item_dist(cnx):

    cursor = cnx.cursor()
    add_item = ("INSERT INTO item_dist(item_id, p_name, date_recieved)"
                "VALUES(%s, %s, %s)")

    get_id = ("""SELECT item_id AS item_id
             FROM item
             WHERE item_name = %s""")

    player = input("Enter Player Name: ")
    control = int(input("Enter number of entries: "))

    for x in range(control):

        item = input("Enter Item Name: ")

        cursor.execute(get_id, (item,))

        itemid = cursor.fetchone()

        data_item = (itemid[0], player, input("Enter Date Here ex.'YYYY-MM-DD': "))

        cursor.execute(add_item, data_item)
        cnx.commit()

    cursor.close()

def item(cnx):

    cursor = cnx.cursor()
    add_item = ("INSERT INTO item(item_id, item_name, dungeon, is_tier)"
                "VALUES(%s, %s, %s, %s)")

    dungeon = input("Enter Dungeon Name: ")
    tier = input("Enter is_tier: ")
    control = int(input("Enter number of entries: "))

    for x in range(control):

        data_item = (int(input("Enter Item ID: ")), input("Enter Item Name: "), dungeon, tier)

        cursor.execute(add_item, data_item)
        cnx.commit()

    cursor.close()


if __name__ == '__main__':
    main()
