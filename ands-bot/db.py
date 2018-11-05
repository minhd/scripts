import sqlite3
import config


def insert(ro_id):
    sqlite_file = config.db
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('insert into ro values (?,?,?)', (ro_id, False, 0))
    conn.commit()
    conn.close()


def touch(ro_id, duration):
    sqlite_file = config.db
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('update ro set done = ?, duration = ? where id = ?', (True, duration, ro_id))
    conn.commit()
    conn.close()


def schema():
    sqlite_file = config.db
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE ro (id text, done boolean, duration int)''')
    conn.commit()
    conn.close()


def not_done():
    sqlite_file = config.db
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('''select id from ro where done = False''')
    rows = c.fetchall()
    conn.close()
    ids = []
    for row in rows:
        ids.append(row[0])
    return ids


if __name__ == "__main__":
    """
    build the database and schema
    python db.py
    """
    schema()
    # insert(123)
    # touch(123, 444)
