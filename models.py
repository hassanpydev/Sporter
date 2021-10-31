from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class news(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    date = db.Column(db.String(50))
    published = db.Column(db.Boolean)
