from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
import os

#flask shell

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/create', methods=['POST'])
def create_post():
  data = request.json
  title = data.get('title')
  content = data.get('content')
  category = data.get('category')
  tags = data.get('tags')
  
  user = User(title=title, content=content, category=category)

  db.session.add(user)
  db.session.commit()
  return {"status": "recieved"}, 200


if __name__ == "__main__":
  with app.app_context():
    db.create_all()
     
  app.run(debug=True, port=5000)