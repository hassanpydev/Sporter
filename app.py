from flask import Flask
from models import news, db
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/newser"
db.init_app(app)
Migrate(app, db)


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


if __name__ == "__main__":
    app.run()
