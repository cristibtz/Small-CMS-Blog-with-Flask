from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from werkzeug.utils import secure_filename
import os
from .models import Post
from flask_login import login_required

create_post = Blueprint('create_post', __name__)
display_post = Blueprint('display_post', __name__)
delete_post = Blueprint('delete_post', __name__)
edit_post = Blueprint('edit_post', __name__)
upload_image = Blueprint('upload_image', __name__)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/photos')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@create_post.route('/', methods=['GET', 'POST'])
@login_required
def create_post_view():
    if request.method == 'POST':
        new_post = Post(title=request.form.get("title"),description= request.form.get("description"), 
                        content=request.form.get("content"), category=request.form.get("category"), 
                        CTF_website=request.form.get("CTF_website"))
        db.session.add(new_post)
        db.session.commit()
        return "Post Created!"
    return render_template('create_post.html', title="Create Post")

#edit post

@edit_post.route("/<string:title>", methods=['POST', 'GET'])
@login_required
def edit(title):
    if request.method == 'POST':
        post = Post.query.filter_by(title=title).first()
        post.title = request.form.get("title")
        post.description = request.form.get("description")
        post.content = request.form.get("content")
        post.category = request.form.get("category")
        post.CTF_website = request.form.get("CTF_website")
        db.session.commit()
        return redirect(url_for('display_post.post', title=post.title))
    elif request.method == 'GET':
        post = Post.query.filter_by(title=title).first()
        if not post:
            return "Post not found!"
        return render_template('dashboard/edit.html', post=post)

#delete post
@delete_post.route("/<string:title>")
@login_required
def delete(title):
    post = Post.query.filter_by(title=title).first()
    if not post:
        return "Post not found!"
    db.session.delete(post)
    db.session.commit()
    return render_template('dashboard/main.html', title="Dashboard")


@display_post.route("/<string:title>")
def post(title):
    data = Post.query.filter_by(title=title).first()
    if not data:
        return "Post not found!"
    return render_template('post.html', title=data.title, content=data.content, description=data.description, category=data.category, CTF_website=data.CTF_website)

@display_post.route("all")
@login_required
def all_posts():
    data = Post.query.all()
    if not data:
        return "No posts found!"
    return render_template('dashboard/all_posts.html', posts=data)


@upload_image.route('/', methods=['POST', 'GET'])
@login_required
def upload_img():

    if 'image' not in request.files:
        return 'No file part'
    
    file = request.files['image']

    if file.filename == '':
        return 'No selected file'
    
    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        file.save(os.path.join(UPLOAD_FOLDER, filename))

        return redirect(url_for('main_routes.dashboard'))
    else:
        print('Error uploading file')
        return redirect(request.url)