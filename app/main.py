from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import redirect

from app.models.account import Account
from app.models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = "wireless"
account = Account()
login_manager = LoginManager()
bootstrap = Bootstrap(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(email):
    """Load user object using supplied email"""
    return account.check_user(email)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("userdashboard.html", name=current_user)
    else:
        return redirect("login")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            user = account.check_user(request.form['email'])
            if user:
                # A User Exist with that Email now check password
                if request.form['psw'] == user.password:
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    print("Not OK")
                    return "Invalid Username Or Password"
                    # flash("Invalid Username Or Password")
            else:
                return "User Doesn't Exist"

    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    global account
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            if account.check_user(request.form['email']):
                # User Exist
                return "User Already Exists"
            else:
                account.create_user(User(request.form['username'], request.form['email'], request.form['psw']))
                return redirect("login")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/create_shoppinglist")
@login_required
def create_shopping_lst():
    return render_template("create_shoppinglist.html")


@app.route("/invalid")
def invalid():
    return render_template("invalid_creds.html")


if __name__ == '__main__':
    app.run(debug=True)
