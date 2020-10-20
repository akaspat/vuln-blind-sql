import sqlite3

users = [
    ('0', 'fred', 'qwe1'),
    ('1', 'john', '123'),
    ('2', 'alex', 'qwerty'),
    ('3', 'max', 'max456'),
    ('4', 'FoXX', 'mysecret'),
]

def create_db_and_get_cursor(filename):
    conn = sqlite3.connect(filename)
    return conn.cursor()

def initDB(cur):
    #create table users
    try:
        cur.execute("""CREATE TABLE users (
      id int PRIMARY KEY,
      username text NOT NULL,
      password text NOT NULL
      )""")
    except sqlite3.OperationalError:
        print('Table already exists')
        print('Start insertion data...')

    #insert users info
    cur.executemany("INSERT INTO users VALUES (?,?,?)", users)
    print('End insertion data')
    print('DB is init')

def show_all_users(cur):
    print('Data in table users')
    cur.execute("""SELECT * FROM users""")
    _users = cur.fetchall()
    show_answer(_users)

def show_answer(answer):
    for u in answer:
        print('id:', u[0])
        print('username: ', u[1])
        print('password:', u[2])
        print('-------------------------')

#vuln zone
def check(cur, id):
    query = "SELECT * FROM users WHERE id={0}".format(id)
    cur.execute(query)
    print(cur.fetchall())


def run(cur):
    id = input('Input user id: ')
    check(cur, id)


if __name__ == '__main__':
    cur = create_db_and_get_cursor("veryImportant.db")
    initDB(cur)
    show_all_users(cur)
    while True:
        run(cur)

