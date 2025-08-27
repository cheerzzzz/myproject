from flask import Flask, render_template

app = Flask(__name__)

@app.route("/<name>")
def home(name):
    # 仮のユーザーデータ（本当はDBやログイン情報から取得する）
    user = {
        "name": name,
        "role": "admin"   # ここを "user" に変えるとマイページへリンクが出る
    }
    fruits = ["Apple", "Banana", "Orange"]
    return render_template("index.html", name=name, fruits=fruits, user=user)

if __name__ == "__main__":
    app.run(debug=True)