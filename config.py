USERNAME, PASSWORD, HOST, DATABASE_NAME = "MyUser", "MyPassword", "localhost", "Users"

class Config:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}'
    SECRET_KEY = "MySecretKey"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False  
    MAIL_USE_SSL = True  
    MAIL_USERNAME = 'disheat4u@gmail.com'  
    MAIL_PASSWORD = 'zgqbhmrbxjbzbfuk'  
    MAIL_DEFAULT_SENDER = 'disheat4u@gmail.com'  