from flask import Flask
from flask_cors import CORS  # import CORS

app = Flask(__name__)
CORS(app)  # enable CORS for all routes

@app.route("/")
def hello():
    return {"message": "Hello from backend"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)