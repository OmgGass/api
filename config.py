class DevelopmenteConfig():
    Debug = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'admin'
    MYSQL_PASSWORD = '123456'
    MYSQL_DB = 'api_flask'


config = {
    "development" : DevelopmenteConfig
}