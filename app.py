from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    user = {
        "name": "Guest",
        "role": "admin"
    }
    # 仮のメモリスト（本来はDBやフォームから取得する）
    memos = [
        "Buy milk",
        "Finish Flask project",
        "Call Alice"
    ]
    return render_template("index.html", user=user, memos=memos)

if __name__ == "__main__":
    app.run(debug=True)