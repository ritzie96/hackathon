from app import train
from app.models import User, Employee
from app.forms import LoginForm, RegisterForm, SearchForm
from app import app, login, db
from random import randint
from flask import render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask_sqlalchemy import *
from wtforms.validators import ValidationError
import os
import shutil

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data, municipality=form.municipality.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('search'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
        except:
            flash(f'User does not exist', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('search')
            return redirect(next_page)

    return render_template('login.html', title='Login', form=form)

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()

    if form.validate_on_submit():
        if form.search.data:
            municipality = form.municipality.data
            keyss = form.keywords.data
            result = []

            def return_ids(muni):
                ids = []
                try:
                    for cv_ob in Employee.query.filter_by(municipality=muni).all():
                        ids.append(cv_ob.id)
                except Exception as e:
                    pass
                return ids

            filters = []
            if municipality != '':
                filters = return_ids(municipality)            

            if len(keyss) == 0 and filters == []:
                flash(f'Choose some values', 'warning')
                result = []
            elif len(keyss) == 0 and filters != []:
                for i in filters:
                    db_ob = Employee.query.filter(Employee.id == int(i)).first()
                    result.append({'name':db_ob.name,
                        'distance': str(randint(1, 50))+ ' km',
                        'email': db_ob.email,
                        'role': db_ob.role
                        })
            elif len(keyss) != 0:
                ob3 = train.vector_cos(False)
                res3 = ob3.get_results(filters, keyss)
                for i in res3:
                    db_ob = Employee.query.filter(Employee.id == int(i)).first()
                    result.append({'name':db_ob.name,
                        'distance': str(randint(1, 50))+ ' km',
                        'role': db_ob.role
                        })

            if len(result) == 0:
                result = [(0, 'No match found.')]
            return render_template('search.html', form=form, results=result)

    return render_template('search.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))
