import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"  # セッション管理用の秘密鍵（任意の文字列）

# --- DB接続設定 ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///memoapp.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)   # ★ここを忘れない！

# --- Flask-Login & Bcrypt 初期化 ---
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # 未ログイン時にログインページへ飛ばす

# --- アップロード設定 ---
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# --- モデル定義 ---
class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)   # タイトル30文字
    content = db.Column(db.Text, nullable=False)       # 詳細は無制限
    image = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- トップページ ---
@app.route("/")
@login_required
def home():
    memos = Memo.query.all()
    return render_template("index.html", user=current_user, memos=memos)

# --- 新規登録（メモ） ---
@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":
        title = request.form["title"].strip()
        content = request.form["content"].strip()

        # ✅ バリデーション
        if len(title) > 30:
            return "タイトルは30文字以内にしてください"
        if len(content) > 300:
            return "詳細は300文字以内にしてください"

        file = request.files.get("image")
        image_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            image_path = f"/static/uploads/{filename}"

        new_memo = Memo(title=title, content=content, image=image_path)
        db.session.add(new_memo)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("register.html")

# --- 編集ページ ---
@app.route("/edit/<int:memo_id>", methods=["GET", "POST"])
@login_required
def edit(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    if request.method == "POST":
        memo.title = request.form["title"]
        memo.content = request.form["content"]

        file = request.files.get("image")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            memo.image = f"/static/uploads/{filename}"

        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", memo=memo)

# --- メモ削除 ---
@app.route("/delete/<int:memo_id>", methods=["POST"])
@login_required
def delete_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    db.session.delete(memo)
    db.session.commit()
    return redirect(url_for("home"))

# --- ユーザー新規登録 ---
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        # 👇 登録後にログインしてしまう
        login_user(new_user)

        return redirect(url_for("home"))
    return render_template("signup.html")

# --- ログイン ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            return "Invalid username or password"
    return render_template("login.html")

# --- ログアウト ---
@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# --- アプリ起動 & 初期化 ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001, debug=True)
