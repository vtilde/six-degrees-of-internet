import os
import json
import sqlite3

DB_PATH = "degrees/data.db"
PEOPLE_JSON_PATH = "degrees/static/people.json"

try:
    os.remove(DB_PATH)
except FileNotFoundError:
    pass

con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS people (id TEXT PRIMARY KEY, name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS groups (id TEXT PRIMARY KEY, name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS connections (person1 TEXT, person2 TEXT, via TEXT)")
con.commit()

people = os.listdir(os.path.join("data", "people"))
for i in people:
    data = json.load(open(os.path.join("data", "people", i), "r"))
    cur.execute("INSERT INTO people VALUES (?, ?)", (
        data["id"],
        data["name"]
    ))


groups = os.listdir(os.path.join("data", "groups"))
for i in groups:
    group_data = json.load(open(os.path.join("data", "groups", i), "r"))
    cur.execute("INSERT INTO groups VALUES (?, ?)", (
        group_data["id"],
        group_data["name"]
    ))
    for member in group_data["members"]:
        cur.execute("SELECT EXISTS (SELECT 1 FROM people WHERE id=?)",
            (member["id"],)
        ) # (1) if member exists, (0) if not
        if not cur.fetchone()[0]:
            cur.execute("INSERT INTO people VALUES (?, ?)", (
                member["id"],
                member["id"]
            ))
        member_connections = [x for x in group_data["members"] if x != member]
        for j in member_connections:
            cur.execute("INSERT INTO connections VALUES (?, ?, ?)", (
                member["id"],
                j["id"],
                group_data["id"]
            ))

con.commit()

# json file for list of all people
people = []
cur.execute("SELECT * FROM PEOPLE")
for i in cur.fetchall():
    people.append({
        "id": i[0],
        "name": i[1]
    })
with open(PEOPLE_JSON_PATH, "w") as f:
    json.dump(people, f)