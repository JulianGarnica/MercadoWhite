class Test():

  def __init__(self, app):
      self.appVar = app
  # The actual decorator function
  def methods(self):
    app = self.appVar

    @app.route("/")
    def hello():
      return "Hello World!"