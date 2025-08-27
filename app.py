from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- DB接続設定 ---
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:sxax0308x@localhost/memoapp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- モデル定義 ---
class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)          # タイトル
    content = db.Column(db.Text, nullable=False)               # 本文
    image = db.Column(db.String(300))                          # 画像URL
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())  # 作成日時
    height = db.Column(db.Integer)                             # 画像の高さ(px)

# --- ルーティング ---
@app.route("/")
def home():
    user = {"name": "Guest", "role": "admin"}
    memos = Memo.query.all()   # DBから全件取得
    return render_template("index.html", user=user, memos=memos)

# --- アプリ起動 & 初期化 ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 初回だけテーブル作成

        # テストデータ（最初だけ）
        if not Memo.query.first():
            sample_memos = [
                Memo(title="Buy milk", content="Go to store", 
                     image="https://i.postimg.cc/sxcxRpcM/park-7407081-1280.jpg", height=300),
                Memo(title="Finish Project", content="Work on Flask app", 
                     image="https://i.postimg.cc/TYdhJ4dg/wedding-1867547-1280.jpg", height=400),
                Memo(title="Call Alice", content="Discuss weekend plan", 
                     image="https://i.postimg.cc/YCV9k21z/wedding-1850074-1280.jpg", height=250),
                Memo(title="Read Book", content="Study Python", 
                     image="https://i.postimg.cc/Pf45JQWx/bride-6230410-1280.jpg", height=350),
            ]
            db.session.add_all(sample_memos)
            db.session.commit()

    app.run(host="0.0.0.0", port=5001, debug=True)

