from datetime import datetime

from flask import flash, redirect, url_for, jsonify
from flask import render_template, abort, make_response
from flask import request
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from sqlalchemy import text
from werkzeug.urls import url_parse

from app import app, db
from app.forms import EditProfileForm
from app.forms import LoginForm
from app.forms import RegistrationForm, AnnouncementForm, EditAnnForm
from app.models import User, Announcement


@app.route('/')
@app.route('/index')
@login_required
def index():
    """
    Rendering main page with all announces.
    :return:
    """
    result = db.engine.execute(text("select * from announcement"))
    anns = []
    for row in result:
        element = dict()
        try:
            userr = User.query.filter_by(id=row.user_id).first()
            element['author'] = {'username': userr.username, 'email': userr.email}
        except:
            element['author'] = {'username': 'Err uid: : ' + str(row.user_id)}
        element['body'] = row.body
        element['name'] = row.name
        element['price'] = row.price
        element['timestamp'] = row.timestamp.split('.')[0]
        element['id'] = row.id
        anns.append(element)
    return render_template("index.html", title='Ads', posts=sorted(anns, key=lambda x: x['timestamp'], reverse=True))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Render login page and moves to index.
    :return:
    """
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
    return render_template('login.html', title='Zaloguj', form=form)


@app.route('/logout')
def logout():
    """
    Close current section
    :return:
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Sign up users to database user model.
    :return:
    """
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
    return render_template('register.html', title='Rejestracja', form=form)


@app.route('/user/<username>', methods=['GET', 'PUT'])
@login_required
def user(username):
    """
    Rendering user by username and handles his profile page
    :param username:
    :return:
    """
    u = User.query.filter_by(username=username).first_or_404()
    result = db.engine.execute(text('select * from announcement where user_id= :usrn'), usrn=u.id)
    anns = [row for row in result]
    return render_template('user.html', user=u, posts=anns)


@app.before_request
def before_request():
    """
    Auth check
    :return:
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Rendering form-page to edit profile info (about me etc) browser
    :return:
    """
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
    return render_template('edit_profile.html', title='Edytuj Profil',
                           form=form)


@app.route('/add_announcement', methods=['GET', 'POST'])
@login_required
def add_announcement():
    """
    Adding new announcement in browser by routing to other temp-form
    :return:
    """
    form = AnnouncementForm()
    if form.validate_on_submit():
        u = Announcement(body=form.body.data, name=form.name.data, price=form.price.data, user_id=current_user.id)
        db.session.add(u)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('add_announcement'))
    return render_template('add_announcement.html', title='Dodaj ogłoszenie',
                           form=form)


@app.route('/edit_announcement', methods=['GET', 'POST'])
@login_required
def edit_announcement():
    """
    Allow user to edit announcement in browser.
    :return:
    """
    form = EditAnnForm()
    if form.validate_on_submit():
        Announcement.query.filter_by(user_id=current_user.id).filter_by(id=form.id.data).update(
            dict(body=form.body.data, name=form.name.data, price=form.price.data))
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_announcement'))
    return render_template('edit_announcement.html', title='Edytuj ogłoszenie',
                           form=form)


@app.route('/user/<username>', methods=['POST'])
@login_required
def delete_announcement(username, flag=False):
    """
    Allow user to delete his announcement(browser)
    :param username:
    :param flag:
    :return:
    """
    rs = db.engine.execute('select id from user where username =:u', u=username)
    z = None
    for x in rs:
        if int(x[0]) == x[0]:
            z = x[0]
    if z:
        val = request.form['zxc']
        db.engine.execute('delete from announcement where id =:v and user_id =:ui', ui=z, v=val)
        db.session.commit()
        del z
    if not flag:
        return user(username)


@app.route('/user/<username>', methods=['DELETE'])
def delete_account(username):
    """
    Allow user to delete account (browser)
    :param username:
    :return:
    """
    try:
        rs = db.engine.execute('select id from user where username =:u', u=username)
        z = None
        for x in rs:
            if int(x[0]) == x[0]:
                z = x[0]
        if z:
            db.engine.execute('delete from announcement where user_id =:v', v=z)
            db.session.commit()
            db.engine.execute('delete from user where id =:ui', ui=z)
            db.session.commit()
        return make_response(' ', 204)
    except:
        return abort(409)


@app.route('/user/<username>', methods=['GET'])
def get_account(username):
    """
    Simple select- get -read for user. ( tests - postman)
    :param username:
    :return:
    """
    try:
        rs = db.engine.execute('select * from user where username =:u', u=username)
        db.session.commit()
        return jsonify(rs)
    except:
        return abort(400)


@app.route('/anns/<idx>', methods=['GET'])
def get_anon(idx):
    """
    GET request handling for announcement.
    If json as response is needed just uncomment line and coment template rendering line
    :param idx:
    :return:
    """
    try:
        rs = db.engine.execute('select * from announcement where id =:u', u=idx).first()
        r = [x for x in rs]
        d = dict(id=r[0], name=r[-1], timestamp=r[3].split('.')[0], body=r[1], price=r[2], user_id=r[-2])
        try:
            rs = db.engine.execute('select * from user where id =:u', u=r[-2]).first()
            r = [x for x in rs]
            usr = dict(name=r[1], email=r[2], timestamp=r[-1].split('.')[0])
        except:
            usr = dict(name='Not found', email='Not found', timestamp='Not found')
        # return jsonify(d)
        return render_template("announce.html", test=d, user=usr)
    except:
        return abort(400)


@app.route('/anns/<idx>', methods=['DELETE'])
def del_anon(idx):
    """
    Handling for crud DELETE request on announcement.
    :param idx:
    :return:
    """
    try:
        db.engine.execute('delete from announcement where id =:u', u=idx)
        return make_response(' ', 204)
    except:
        return abort(400)


@app.route('/anns/<idx>', methods=['POST'])
def post_anon(idx):
    """
    Handling for posting - inserting new announces.
    :param idx:
    :return:
    """
    args = request.json
    if args:
        args['id'] = idx
        a = Announcement(**args)
        db.session.add(a)
        db.session.commit()
        return make_response(jsonify(args), 201)
    return abort(400)


@app.route('/anns/<idx>', methods=['PUT'])
def put_anon(idx):
    """
    Handling for PUT - updating announcement.
    :param idx:
    :return:
    """
    args = request.json
    if args:
        Announcement.query.filter_by(id=idx).update(args)
        db.session.commit()
        return make_response(jsonify({'url': 'http://127.0.0.1:5000/anns/' + idx}), 201)
    return abort(400)
