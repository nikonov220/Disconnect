import secrets

import telebot

from flask_bcrypt import generate_password_hash, check_password_hash
from flask import (Flask, g, render_template,
                   flash, redirect, url_for,
                   request)
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import models
import forms
import helper

from config import bot_token, flask_secret_key

bot = telebot.TeleBot(bot_token)

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = flask_secret_key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/check'
login_manager.login_message = "login_required"

@login_manager.user_loader
def load_user(uid):
    try:
        return models.User.get(models.User.id == uid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connects to a database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Closes db connection after each request"""
    g.db.close()
    return response


@app.route("/check", methods=('GET', 'POST'))
def check():
    form = forms.LoginForm()
    if form.validate_on_submit():
        uid = form.value.data
        try:
            uid = helper.uid_check(uid)
        except models.DoesNotExist:
            flash("user_not_found")
            form.value.data = ''
            return render_template('login.html', form=form, form_action='', hidden_value="1", text='login')
        password = str(secrets.randbits(20))
        p_hash = generate_password_hash(password)
        models.User.update(temp_password=p_hash).where(models.User.uid == uid).execute()

        # next line is for offline debug
        # form.value.data = password
        bot.send_message(uid, "Your secret code: {}".format(password))
        form.value.data = ''

        return render_template('login.html', form=form, form_action=url_for('login'),
                               hidden_value=uid, text='secret_code')

    return render_template('login.html', form=form, form_action='', hidden_value="1", text='login')


@app.route("/login", methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        password_def = 'not_logging'
        uid = request.form['hidden_value']
        password_try = request.form['value']
        if password_try == password_def:
            flash("ip_banned")
            return redirect(url_for('check'))
        user = models.User.get(models.User.uid == uid)
        try:
            logged = check_password_hash(user.temp_password, password_try)
        except ValueError:
            flash("refresh_error")
            return redirect(url_for('check'))
        if logged:
            login_user(user)
            user.update(temp_password=password_def).execute()
            flash("login_success")
            return redirect(url_for('dashboard'))
        user.update(temp_password=password_def).execute()
        flash("wrong_password")
        return redirect(url_for('check'))
    if request.method == 'GET':
        return redirect(url_for('check'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard'))


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)