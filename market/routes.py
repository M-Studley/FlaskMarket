from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from market import app, db
from market.models import Item, User
from market.forms import RegisterForm, LoginForm


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Logged in Successfully as {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password are incorrect... Please try again...', category='danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        validated_user = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password.data)
        db.session.add(validated_user)
        db.session.commit()
        return redirect(url_for('login_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"ERROR: {err_msg[0]}", category='danger')

    return render_template('register.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('Logged Out Successfully!', category='info')
    return redirect(url_for('login_page'))
