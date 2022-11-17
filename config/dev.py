from .configs import Config


class DevelopmentConfig(Config):
  DEBUG = True

  DB_HOST = "127.0.0.1"
  DB_USERNAME = "root"
  DB_PASSWORD = ""
  DB_PORT = 3306

  IMAGE_UPLOADS = "/uploads"

  SESSION_COOKIE_SECURE = False
  