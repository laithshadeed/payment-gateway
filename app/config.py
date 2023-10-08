import os

class Config:
    # TODO: Move to postgres && db pooling
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///payment.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # TODO: move from memory to redis or memcache with pooling
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = '1000 per minute, 100 per second'
    RATELIMIT_HEADERS_ENABLED = True


