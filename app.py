from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/create', methods=['POST'])
def create_post():
  data = request.json
  print(data)
  return {"status": "recieved"}, 200

if __name__ == "__main__":
  app.run(debug=True, port=5000)