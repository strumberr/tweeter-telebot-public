import sqlite3

con = sqlite3.connect('info_people.db', check_same_thread=False)

def database(chat_id, first_name, last_name):
    with con:

        cur = con.cursor()

        cur.execute("insert into info_people values(?,?,?)",(chat_id, first_name, last_name))
        last_row = cur.execute('select * from info_people').fetchall()[-1]
        print(last_row)

        con.commit()


def create_db():
    with con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE info_people
                (chat_id, first_name, last_name)''')


def database2(chat_id, number_starts):
    with con:

        cur = con.cursor()

        cur.execute("insert into num_start values(?,?)",(chat_id, number_starts))
        last_row = cur.execute('select * from num_start').fetchall()[-1]
        print(last_row)

        con.commit()