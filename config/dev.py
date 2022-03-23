from .configs import Config


class DevelopmentConfig(Config):
  DEBUG = True

  DB_NAME = "development-db"
  DB_USERNAME = "admin"
  DB_PASSWORD = "example"

  IMAGE_UPLOADS = "/home/username/projects/my_app/app/static/images/uploads"

  SESSION_COOKIE_SECURE = False