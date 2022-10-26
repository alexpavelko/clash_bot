import sqlite3

con = sqlite3.connect("db/users.db")
cur = con.cursor()


def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id int PRIMARY KEY,
    tg_id TEXT,
    clash_tag TEXT);
    """)
    con.commit()


def insert(tg_id, clash_tag):
    user = cur.execute("SELECT * FROM users WHERE tg_id = ? AND clash_tag = ?",
                       (str(tg_id), str(clash_tag)))
    if not user.fetchall():
        cur.execute("INSERT INTO users (tg_id, clash_tag) values (?, ?)", [(str(tg_id)), str(clash_tag)])
        con.commit()
        return True
    return False


def get_all():
    return cur.execute(f"SELECT * FROM users")


def get_by_clash_tag(clash_tag):
    user = cur.execute(f"SELECT * FROM users WHERE clash_tag='{clash_tag}'")
    return user


def get_by_tg_id(tg_id):
    user = cur.execute(f"SELECT * FROM users WHERE tg_id='{tg_id}' ")
    return user


def exists_by_tg_id(tg_id):
    users = cur.execute(f"SELECT * FROM users WHERE tg_id='{tg_id}' ")
    if not users.fetchall():
        return False
    return True


def exists_by_clash_tag(clash_tag):
    users = cur.execute(f"SELECT * FROM users WHERE clash_tag ='{clash_tag}'")
    if not users.fetchall():
        return False
    return True


def delete(tg_id):
    cur.execute(f"DELETE FROM users WHERE tg_id={tg_id}")
    con.commit()
    result = cur.execute(f"SELECT * FROM users WHERE tg_id={tg_id}")
    return result