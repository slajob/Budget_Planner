from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, ExpensesForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Expenses
from werkzeug.urls import url_parse
from datetime import datetime
from sqlalchemy import func

@app.route('/')
@app.route('/index')
def index():
    user = {'username': ''}
    posts = [{'author': {'username': 'John'},'body': 'Something'},{'author': {'username': 'Susan'},'body': 'something 2'}]

    return render_template('index.html', title='Home', user=user, posts=posts)

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

@app.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    date = datetime.now()
    monthno = int((datetime.utcnow().strftime("%m")))
    if current_user == user:
        cos = "ZATWIERDZONE"
        return render_template('user.html', user=user, date=date.strftime("%d  %B %Y"), monthno=monthno)
    else:
        cos = "NEGATYWNE"
        return render_template('user_error.html', user=user, cos=cos)

@app.route('/add', methods=['POST'])
def add():
    form = ExpensesForm()
    if form.validate_on_submit():
        user_id = current_user.id
        monthno = form.monthno.data
        new_record = Expenses(name=form.name.data, amount=form.amount.data, user_id=user_id, exorin=form.exorin.data, monthno=monthno)
        if form.exorin.data == "Expense":
            form.amount.data = -form.amount.data
            new_record = Expenses(name=form.name.data, amount=form.amount.data, user_id=user_id, exorin=form.exorin.data, monthno=monthno)
        db.session.add(new_record)
        db.session.commit()
        return redirect('/add')

    return render_template('add.html', title='Add', form=form)

@app.route('/add', methods=['GET'])
def show():
    form = ExpensesForm()
    choosed = form.monthno.data #show records from actual month
    print(choosed)
    exp = Expenses.query.filter(Expenses.monthno == choosed)
    # if monthform.show.data and monthform.validate_on_submit():
    #     choosed = monthform.choosemonth.data
    #     print(choosed)
    #     exp = Expenses.query.filter(Expenses.monthno == choosed)
    #     form = ExpensesForm()
    #     summary = (Expenses.query.with_entities(func.sum(Expenses.amount)).filter(Expenses.monthno == choosed)[0])
    #     return render_template('add.html', title='Add', form=form, monthform=monthform, choosed=choosed, exp=exp, summary=summary)
    #     render_template('add.html', title='Add', form=form, monthform=monthform)
    summary = (Expenses.query.with_entities(func.sum(Expenses.amount)).filter(Expenses.monthno == choosed)[0])
    return render_template('add.html', title='Add', exp=exp, summary=summary, form=form)



