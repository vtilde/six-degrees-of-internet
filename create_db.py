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
cur.execute("CREATE TABLE IF NOT EXISTS people (username TEXT PRIMARY KEY)")
cur.execute("CREATE TABLE IF NOT EXISTS groups (groupname TEXT PRIMARY KEY, grouptype TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS connections (person1 TEXT, person2 TEXT, via TEXT)")
con.commit()

def make_list(data):
    if isinstance(data, dict):
        return [data]
    else:
        return data

people = os.listdir(os.path.join("data", "people"))
for i in people:
    data = make_list(json.load(open(os.path.join("data", "people", i), "r")))
    for person in data:
        cur.execute("INSERT INTO people VALUES (?)", [person["username"]])


groups = os.listdir(os.path.join("data", "groups"))
missing_people = [] # people in groups with dedicated file missing
for i in groups:
    group_file = make_list(json.load(open(os.path.join("data", "groups", i), "r")))
    for group_data in group_file:
        cur.execute("INSERT OR IGNORE INTO groups VALUES (?, ?)", (
            group_data["groupname"],
            group_data["type"]
        ))
        for member in group_data["members"]:
            cur.execute("SELECT EXISTS (SELECT 1 FROM people WHERE username=?)",
                (member["username"],)
            ) # (1) if member exists, (0) if not
            if not cur.fetchone()[0]:
                cur.execute("INSERT INTO people VALUES (?)", [member["username"]])
                if member["username"] not in missing_people:
                    missing_people.append(member["username"])
            member_connections = [x for x in group_data["members"] if x != member]
            for j in member_connections:
                cur.execute("INSERT INTO connections VALUES (?, ?, ?)", (
                    member["username"],
                    j["username"],
                    group_data["groupname"]
                ))

con.commit()
print("missing people files: " + ", ".join(missing_people))

# json file for list of all people
people = []
cur.execute("SELECT * FROM people ORDER BY username")
for i in cur.fetchall():
    people.append({
        "username": i[0]
    })
with open(PEOPLE_JSON_PATH, "w") as f:
    json.dump(people, f)