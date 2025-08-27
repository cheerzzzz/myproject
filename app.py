from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    user = {"name": "Guest", "role": "admin"}
    memos = [
        {"image": "https://i.postimg.cc/sxcxRpcM/park-7407081-1280.jpg", "text": "Buy milk", "height": 300},
        {"image": "https://i.postimg.cc/TYdhJ4dg/wedding-1867547-1280.jpg", "text": "Finish Flask project", "height": 350},
        {"image": "https://i.postimg.cc/YCV9k21z/wedding-1850074-1280.jpg", "text": "Call Alice", "height": 250},
        {"image": "https://i.postimg.cc/Pf45JQWx/bride-6230410-1280.jpg", "text": "Read a book", "height": 400},
        {"image": "https://i.postimg.cc/3Rh3JkWm/love-6600903-1280.jpg", "text": "Workout", "height": 300},
    ]
    return render_template("index.html", user=user, memos=memos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
