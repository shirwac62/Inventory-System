from flask import render_template, url_for, flash, redirect, request
from web.blueprints.login.forms import LoginForm
from web.extensions import bcrypt
from web.blueprints.register.models import User
from flask_login import login_user, current_user
from utility.mkblueprint import ProjectBlueprint

blueprint = ProjectBlueprint('/', __name__)


@blueprint.route(blueprint.url, methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.home'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)


@blueprint.route(blueprint.url + '/about')
def about():
    return render_template('about.html', title='about')
