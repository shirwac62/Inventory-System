import datetime
from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user

from web import app
from web.extensions import db, login_manager, bcrypt, save_to_db

from web.blueprints.register.forms import RegistrationForm
from web.blueprints.register.models import User

from utility.mkblueprint import ProjectBlueprint

blueprint = ProjectBlueprint('register', __name__)


@blueprint.route(blueprint.url, methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        print(user)
        save_to_db(user)
        flash('Your Account has been created', 'success')
        return redirect(url_for('/.login'))
    return render_template('register.html', title='Register', form=form)
