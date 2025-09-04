from flask import request, g
from degrees import app, find_link
import sqlite3

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        g._database = sqlite3.connect(app.config["DB_PATH"])
        db = g._database
    return db


@app.route("/")
def index():
    return "hewwo wowld"

@app.route("/search")
def search():
    search_start = request.args.get("start")
    search_end = request.args.get("end")
    if search_start is None or search_end is None:
        return "missing parameters"

    chain = find_link.search(get_db(), search_start, search_end)

    return str(chain)