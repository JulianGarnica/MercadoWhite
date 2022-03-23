from distutils.log import debug
from appName import app
from config import configs

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

#print(f'ENV is set to: {app.config["ENV"]}')

if __name__ == "__main__":
  app.run(debug=app.config["DEBUG"])