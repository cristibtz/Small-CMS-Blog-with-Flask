from flask import Blueprint, render_template, request,redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, current_user, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=False)
                return redirect(url_for('main_routes.dashboard'))
            else:
                return 'Stop trying!'
        else:
            return 'Stop trying!'
    return render_template('login.html') 


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

'''
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return 'Missing username or password'
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='scrypt'))  
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('create_post.create_post_view'))

    return render_template('signup.html')
'''