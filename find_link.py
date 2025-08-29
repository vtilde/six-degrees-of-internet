import sqlite3

DB_NAME = "data.db"

con = sqlite3.connect(DB_NAME)
cur = con.cursor()


def search(start, end):
    queue = []
    searched = []
    queue.append(start)
    while len(queue) > 0:
        cur.execute("SELECT * FROM connections WHERE person1 = ?",
                    (queue.pop(0),))
        print("result", cur.fetchall())
        return


running = True
while running:
    search_start = input("from: ")
    search_end = input("to: ")
    search(search_start, search_end)
