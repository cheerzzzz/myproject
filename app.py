from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Flask!"

@app.route("/guri")
def guri():
    return "Hello, guri!"

@app.route("/gura")
def gura():
    return "Hello, gura!"

if __name__ == "__main__":
    app.run(debug=True)
