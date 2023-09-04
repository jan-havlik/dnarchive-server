import os

from decouple import config

from pydantic_settings import BaseSettings

class DatabaseConfig(BaseSettings):
    db_prefix: str
    db_user: str
    db_password: str
    db_name: str

    @classmethod
    def from_env(cls):
        return cls(
            db_prefix="mongodb+srv://",
            db_user="dnarchive",
            db_password=config("DB_PASSWORD"),
            db_name="db-mongodb-fra1-44245-3eedce86.mongo.ondigitalocean.com/dnarchive?authSource=admin&replicaSet=db-mongodb-fra1-44245&tls=true",
        )

# Create an instance of DatabaseConfig using environment variables.
db_config = DatabaseConfig.from_env()
