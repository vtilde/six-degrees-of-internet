import os
import json
import sqlite3

DB_NAME = "data.db"

con = sqlite3.connect(DB_NAME)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS people (id TEXT PRIMARY KEY, name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS groups (id TEXT PRIMARY KEY, name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS connections (personId TEXT, groupId TEXT, type TEXT)")
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
    data = json.load(open(os.path.join("data", "groups", i), "r"))
    cur.execute("INSERT INTO groups VALUES (?, ?)", (
        data["id"],
        data["name"]
    ))
    for member in data["members"]:
        cur.execute("INSERT INTO connections VALUES (?, ?, ?)", (
            member["id"],
            data["id"],
            member["type"]
        ))

con.commit()