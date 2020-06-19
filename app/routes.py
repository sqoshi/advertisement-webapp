from datetime import datetime

from flask import flash, redirect, url_for
from flask import render_template
from flask import request
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from sqlalchemy import text
from werkzeug.urls import url_parse

from app import app, db
from app.forms import EditProfileForm
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    usrs = dict()
    result = db.engine.execute(text("select * from user"))
    for row in result:
        usrs[row.id] = row.username
    print(usrs)
    result = db.engine.execute(text("select * from announcement"))
    anns = []
    for row in result:
        element = dict()
        element['author'] = {'username': usrs[row.id]}
        element['body'] = row.body
        element['name'] = row.name
        element['price'] = row.price
        element['timestamp'] = row.timestamp
        anns.append(element)
    return render_template("index.html", title='Ads', posts=anns)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    u = User.query.filter_by(username=username).first_or_404()
    result = db.engine.execute(text('select * from announcement where user_id= :usrn'), usrn=u.id)
    anns = [row for row in result]
    return render_template('user.html', user=u, posts=anns)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
