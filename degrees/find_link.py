import sqlite3
from degrees import search_utils

def search(db, start, end):
    cur = db.cursor()
    q = search_utils.Queue()
    q.explore(start, None, None)
    q.enqueue(start)
    while len(q.queue) > 0:
        current_node = q.dequeue()
        if current_node == end:
            break
        cur.execute("SELECT * FROM connections WHERE person1 = ?",
                    (current_node,))
        for i in cur.fetchall():
            if i[1] not in q.explored:
                q.explore(i[1], current_node, i[2])
                q.enqueue(i[1])

    path = q.get_path(current_node)
    # print(current_node)
    # for i in path._path:
    #     print(i.node, i.link)
    return path._path

if __name__ == "__main__":
    DB_NAME = "data.db"
    running = True
    con = sqlite3.connect(DB_NAME)
    while running:
        search_start = input("from: ")
        search_end = input("to: ")
        print(search(con, search_start, search_end))
        break
