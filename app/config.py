class Config(object):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE = {"url": "sqlite:///company.sqlite"}


class TestConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE = {"url": "sqlite:///test.sqlite"}
