from pydantic_settings import BaseSettings
from app.services.enums.base import StrEnum


class APIConfig(BaseSettings):
    VERSION: str = '0.0.0'
    TITLE: str = 'Special Equipment API'
    SUMMARY: str | None = None
    DESCRIPTION: str = 'Special equipment sales system API'
    PREFIX: str = '/api'
    IS_VISIBLE: bool = False

    class Config:
        env_prefix = 'API_'
        env_file = '.env'

class DBConfig(BaseSettings):
    ALEMBIC_INI_PATH: str = 'alembic.ini'
    PORT: int = 5432
    HOST: str = 'special_equipment_postgres'
    NAME: str = 'special_equipment'
    USER: str = 'admin'
    PASS: str = 'password'
    APPLY_MIGRATIONS: bool = True

    def dsn(self):
        return f"postgresql://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"
    
    class Config:
        env_prefix = 'DB_'
        env_file = '.env'

class AppConfig(BaseSettings):
    PORT: int = 80
    HOST: str = '0.0.0.0'
    DEBUG: bool = False

    class Config:
        env_prefix = 'APP_'
        env_file = '.env'

class LogConfig(BaseSettings):
    class LogLevelEnum(StrEnum):
        debug = 'DEBUG'
        info = 'INFO'
        error = 'ERROR'

    LEVEL: LogLevelEnum = LogLevelEnum.info
    TO_FILE: bool = True
    LOG_DIR: str = 'logs'
    RETENTION: int = 5
    ROTATION: int = 100

    class Config:
        env_prefix = 'LOG_'
        use_enum_values = True
        env_file = '.env'

class AuthConfig(BaseSettings):
    SECRET_KEY: str = 'secret_key'
    ACCESS_TOKEN_EXPIRE: int = 3600
    ALGORITHM: str = 'HS256'
    class Config:
        env_prefix = 'AUTH_'
        env_file = '.env'


class Config(BaseSettings):
    api: APIConfig = APIConfig()
    db:  DBConfig  = DBConfig()
    app: AppConfig = AppConfig()
    log: LogConfig = LogConfig()
    auth: AuthConfig = AuthConfig()
