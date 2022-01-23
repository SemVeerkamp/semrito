from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Ingelogd!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Deze naam bestaat niet. Meld je eerst aan voordar je inlogt', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('Name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(name=name).first()
        if user:
            flash('Deze naam bestaat al, kies een andere naam en probeer het opnieuw.', category='error')
        elif len(name) < 4:
            flash('Kies een naam die langer is dan 3 tekens', category='error')
        elif password1 != password2:
            flash('Wachtwoord 1 en wachtwoord 2 zijn niet hetzelfde', category='error')
        elif len(password1) < 7:
            flash('Kies een wachtwoord dat langer is dan 7 tekens', category='error')
        else:
            new_user = User(name=name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
