from distutils.log import debug
from appPool import app as appPool

#print(f'ENV is set to: {app.config["ENV"]}')
#Change Env: export FLASK_ENV=development

if __name__ == "__main__":
  appPool.run(debug=appPool.config["DEBUG"])