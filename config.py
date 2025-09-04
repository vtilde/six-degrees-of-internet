import os

class Config:
    DB_PATH = os.environ.get("DB_PATH", "degrees/data.db")