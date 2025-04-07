from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
import json
import os

#flask shell

# curl -X POST http://localhost:5000/create \
#   -H "Content-Type: application/json" \
#   -d '{
#     "title": "Tagged Post",
#     "content": "This one has tags stored in JSON.",
#     "category": "Tutorial",
#     "tags": ["flask", "api", "sqlite"]
# }'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_tags(self, tag_list):
      self.tags = json.dumps(tag_list)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": json.loads(self.tags) if self.tags else [],
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat()
        }


@app.route('/')
def home():
  return render_template("index.html")

@app.route('/posts', methods=['POST'])
def create_post():
  data = request.json
  title = data.get('title')
  content = data.get('content')
  category = data.get('category')
  tags = data.get('tags')
  
  user = User(title=title, content=content, category=category)
  temp = []
  for x in tags:
    temp.append(x)
  user.set_tags(temp)

  db.session.add(user)
  db.session.commit()
  return {"status": "recieved"}, 200

@app.route('/view', methods=['GET'])
def view_post():
  user_id = request.args.get("id")
  if not user_id:
    return {"error": "Missing 'id' parameter"}, 400
  user = User.query.get(user_id)
  print(user)
  return {"title": user.title, "content": user.content, "category": user.category, "tags": user.tags, "createdAt":user.created_at, "updatedAt": user.updated_at}, 200

@app.route('/view/all', methods=['GET'])
def view_all():
  users = [u.to_dict() for u in User.query.all()]
  return {"users": users}, 200

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update(post_id):
  user = User.query.get(post_id)
  data = request.json
  
  title = data.get('title')
  content = data.get('content')
  category = data.get('category')
  tags = data.get('tags')

  user.title = title
  user.content = content
  user.category = category
  user.tags = tags

  db.session.commit()

  return {"status": "recieved"}, 200

if __name__ == "__main__":
  with app.app_context():
    db.create_all()
     
  app.run(debug=True, port=5000)