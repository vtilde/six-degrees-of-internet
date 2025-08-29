import os
import json
import sqlite3

DB_NAME = "data.db"

con = sqlite3.connect(DB_NAME)
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
        member_connections = [x for x in group_data["members"] if x != member]
        print(member, member_connections)
        for j in member_connections:
            cur.execute("INSERT INTO connections VALUES (?, ?, ?)", (
                member["id"],
                j["id"],
                group_data["id"]
            ))

        # cur.execute("INSERT INTO connections VALUES (?, ?, ?)", (
        #     member["id"],
        #     group_data["id"],
        #     member["type"]
        # ))

con.commit()