USERNAME, PASSWORD, HOST, DATABASE_NAME = "MyUser", "MyPassword", "localhost", "Users"

class Config:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}'
    SECRET_KEY = "MySecretKey"
