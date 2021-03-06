import sqlite3

users = [
    ('0', 'fred', 'qwe1'),
    ('1', 'john', '123'),
    ('2', 'alex', 'qwerty'),
    ('3', 'max', 'max456'),
    ('4', 'FoXX', 'mysecret'),
]

blacklist = ['or', 'and', 'select', '||', 'union', 'delete',
             'drop', 'update', '==', '=', '--', '#', '\'', '\"',
             'create', ' ']

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
    cur.executemany("INSERT INTO users VALUES (?, ?, ?)", users)
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
def check(_cur, _id):
    result = True

    ids = _cur.execute("SELECT id FROM users").fetchall()
    for element in ids:
        if str(_id) == str(element[0]):
            print('User exists')
            break

    # to lowercase
    _id = _id.lower()

    # remove symbols from blacklist
    for black_element in blacklist:
        if black_element in _id:
            _id = _id.replace(black_element, "")
            result = False

    # remove alphabet symbols. allow only digits
    for c in _id:
        if c.isalpha():
            _id = _id.replace(c, "")
            result = False

    # check is empty
    if not len(_id):
        result = False

    if result:
        answer = _cur.execute("SELECT * FROM users WHERE id={0}".format(_id)).fetchall()
        if len(answer):
            print('User exists')

def run(_cur):
    _id = input('Input user id: ')
    check(_cur, _id)


if __name__ == '__main__':
    cur = create_db_and_get_cursor("veryImportant.db")
    initDB(cur)
    while True:
        run(cur)


