import sqlite3

DB_NAME = "data.db"

def search(db, start, end):
    cur = db.cursor()
    queue = []
    explored = {} # "id": "parent"
    queue.append(start)
    explored[start] = None
    while len(queue) > 0:
        current_node = queue.pop(0)
        if current_node == end:
            print("found")
            break
        cur.execute("SELECT * FROM connections WHERE person1 = ?",
                    (current_node,))
        for i in cur.fetchall():
            if i[1] not in explored:
                explored[i[1]] = current_node
                queue.append(i[1])
    print("explored:", explored)
    # record path (from end)
    path = []
    tracing = True
    while tracing:
        path.append(current_node)
        current_node = explored[current_node]
        if current_node is None:
            return path

if __name__ == "__main__":
    running = True
    con = sqlite3.connect(DB_NAME)
    while running:
        search_start = input("from: ")
        search_end = input("to: ")
        print(search(con, search_start, search_end))
        break
