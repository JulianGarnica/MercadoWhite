# from werkzeug.serving import run_simple # werkzeug development server
from apps import app

#Env development: export FLASK_ENV=development
if __name__ == '__main__':
   app.run()