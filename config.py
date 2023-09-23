from os import getenv
from dotenv import load_dotenv
from  distutils.util import strtobool


load_dotenv()


class APIConfig:
    API_VERSION =     '0.0.0'
    API_TITLE =       'Special Equipment API'
    API_SUMMARY =     None
    API_DESCRIPTION = 'Special equipment sales system API'
    API_PREFIX =      '/api'
    API_IS_VISIBLE =  bool(strtobool(getenv('API_IS_VISIBLE', default='true')))

class DBConfig:
    DB_PORT =     int(getenv('DB_PORT',     default=5432))
    DB_HOST =         getenv('DB_HOST',     default='special_equipment')
    DB_NAME =         getenv('DB_NAME',     default='special_equipment')
    DB_USER =         getenv('DB_USER',     default='admin')
    DB_PASS =         getenv('DB_PASS',     default='password')

    def dsn(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

class AppConfig:
    APP_SECRET_KEY =                getenv('APP_SECRET_KEY', default='secret_key')
    APP_PORT =                  int(getenv('APP_PORT',       default=80))
    APP_HOST =                      getenv('APP_HOST',       default='0.0.0.0')
    APP_DEBUG =      bool(strtobool(getenv('APP_DEBUG',      default='false')))

class LogConfig:
    LOG_LEVEL = getenv('LOG_LEVEL', default='info')
    LOG_DIR =   getenv('LOG_DIR',   default='log')


class Config(object):
    api_config = APIConfig()
    db_config = DBConfig()
    app_config = AppConfig()
    log_config = LogConfig()
