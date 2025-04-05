from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

#flask shell

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    date_joined = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/create', methods=['POST'])
def create_post():
  data = request.json
  print(data)
  return {"status": "recieved"}, 200

if __name__ == "__main__":
  with app.app_context():
     db.create_all()
  app.run(debug=True, port=5000)