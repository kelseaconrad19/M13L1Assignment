class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:JonJamLil24!@localhost/factory-management-system"
    CACHE_TYPE = "SimpleCache"
    DEBUG = True
    CACHE_DEFAULT_TIMEOUT = 300