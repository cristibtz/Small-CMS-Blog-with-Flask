from flask import Blueprint, render_template
from flask_login import login_required

main_routes = Blueprint('main_routes', __name__)

#Home page
@main_routes.route('/')
def home(title="Home"):
    return render_template('home.html', title=title)

#Projects page
@main_routes.route('/projects')
def projects(title="Projects"):
    return render_template('projects.html', title=title)

#About page
@main_routes.route('/about')
def about(title="About"):
    return render_template('about.html', title=title)

@main_routes.route('/dashboard')
@login_required
def dashboard(title="Dashboard"):
    return render_template('dashboard/main.html', title=title)