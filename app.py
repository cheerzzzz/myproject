import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- DB接続設定 ---
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:sxax0308x@localhost/memoapp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- アップロード設定 ---
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # フォルダがなければ作成

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# --- モデル定義 ---
class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)          # タイトル
    content = db.Column(db.Text, nullable=False)               # 本文
    image = db.Column(db.String(300))                          # 画像パス
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())  # 作成日時

# --- トップページ ---
@app.route("/")
def home():
    user = {"name": "Guest", "role": "admin"}
    memos = Memo.query.all()
    return render_template("index.html", user=user, memos=memos)

# --- 新規登録ページ ---
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        # ファイルの処理
        file = request.files.get("image")
        image_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_path = f"/static/uploads/{filename}"

        # DBに保存
        new_memo = Memo(title=title, content=content, image=image_path)
        db.session.add(new_memo)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("register.html")

# --- アプリ起動 & 初期化 ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001, debug=True)

