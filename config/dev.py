from .configs import Config


class DevelopmentConfig(Config):
  DEBUG = True

  DB_HOST = "82.180.133.59"
  DB_USERNAME = "junian"
  DB_PASSWORD = "01,doctoraguja"
  DB_PORT = 3306

  IMAGE_UPLOADS = "/uploads"

  SESSION_COOKIE_SECURE = False
  