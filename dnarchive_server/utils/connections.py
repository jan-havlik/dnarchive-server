from pymongo import MongoClient

from utils.config import db_config

def get_mongodb():

    client = MongoClient(f"{db_config.db_prefix}{db_config.db_user}:{db_config.db_password}@{db_config.db_name}")
    return client["dnarchive"]
