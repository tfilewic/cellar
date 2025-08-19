import os

ENV = os.getenv("APP_ENV", "local") #default to local

if ENV == "dev":
    SQLALCHEMY_DATABASE_URI = "sqlite:///cellar.db"
elif ENV == "docker":
    DB_HOST = os.getenv("DB_HOST", "db")  #get db host from env or default to docker service "db"
    DB_USER = os.getenv("MYSQL_USER", "cellaruser")
    DB_PASS = os.getenv("MYSQL_PASSWORD", "cellarpass")
    DB_NAME = os.getenv("MYSQL_DATABASE", "cellar")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}"
else:  #local
    DB_USER = os.getenv("MYSQL_USER", "cellaruser")
    DB_PASS = os.getenv("MYSQL_PASSWORD", "cellarpass")
    DB_NAME = os.getenv("MYSQL_DATABASE", "cellar")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@localhost:3306/{DB_NAME}"
