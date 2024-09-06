from flask import Blueprint, render_template, abort


writeups_routes = Blueprint('writeups_routes', __name__)

#Writeup page
@writeups_routes.route('/')
def writeups(title="Writeups"):
    from . import db
    from .models import Post
    ctf_websites = db.session.query(Post.CTF_website).filter(Post.CTF_website != "null").distinct().all()

    return render_template('writeups.html', title=title, ctf_websites=ctf_websites)

@writeups_routes.route('/<website>_writeups')
def website_writeups(website):
    # Import necessary modules
    from . import db
    from .models import Post
    
    # Query all posts for a specific website
    posts = db.session.query(Post).filter(Post.CTF_website == website).all()

    if not posts:  # Check if the posts list is empty
        # Option 1: Abort with a 404 error
        abort(404)
    
    # Group posts by category
    categories_writeups = {}
    for post in posts:
        category = post.category  # Assuming 'category' is an attribute of Post
        if category not in categories_writeups:
            categories_writeups[category] = [post]
        else:
            categories_writeups[category].append(post)
    
    # Pass the grouped data to the template
    return render_template('CTF_website.html', title=website, categories_writeups=categories_writeups, website=website)
