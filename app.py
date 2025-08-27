from flask import Flask, render_template

app = Flask(__name__)

@app.route("/<name>")
def home(name):
    fruits = ["Apple", "Banana", "Orange", "Grapes"]  # リストを用意
    return render_template("index.html", name=name, fruits=fruits)

if __name__ == "__main__":
    app.run(debug=True)
