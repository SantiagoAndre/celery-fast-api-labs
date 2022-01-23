import os
import pathlib
from functools import lru_cache

class BaseConfig:
    BASE_DIR = pathlib.Path(__file__).parent.parent
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3")
    DATABASE_CONNECT_DICT = {}
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    EMAIL_FROM  = os.getenv("EMAIL_FROM")
    EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
    SECRET_KEY=  os.getenv("SECRET_KEY")
    SHA_ALGORITHM = os.getenv("SHA_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    config_name = os.getenv("FASTAPI_CONFIG", "development")
    return config_cls_dict[config_name]()

settings = get_settings()
print(settings.__dict__)
print(os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"))
print(os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"))
print(BaseConfig.DATABASE_URL)