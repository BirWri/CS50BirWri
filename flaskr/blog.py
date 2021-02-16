from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for, escape, current_app, send_from_directory
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db

from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length

import re
import os

from . import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

# retrives all comments connected to posts...
#SELECT username, post_id, author_id, comment_created, comment_body, post_title, post_body, post_created 
#FROM post 
#JOIN user ON post.author_id = user.user_id
#JOIN comments ON comments.OG_post_id = post.post_id ORDER BY post_created DESC



bp = Blueprint('blog', __name__)



@bp.route('/')
def index():
    if g.user is None:
        return render_template('blog/about.html')
    else: 
        db = get_db()
        posts = db.execute(
            'SELECT post_id, post_title, post_body, post_created, author_id, username, post_image'
            ' FROM post JOIN user ON post.author_id = user.user_id'
            ' ORDER BY post_created DESC'
        ).fetchall()

        comments = db.execute(
           'SELECT comment_id, commentor_id, OG_post_id, comment_created, comment_title, comment_body'
            ' FROM comments JOIN post ON comments.OG_post_id = post.post_id'
            ' ORDER BY post_created DESC'
        ).fetchall()
      
        return render_template('blog/index.html', posts=posts, comments = comments)

#def number_of_comments(post_id):

    #db = get_db()
    #number_of_comments = db.execute(
            #'SELECT COUNT (OG_post_id)'
            #' FROM comments'
           # ' WHERE post_id = OG_post_id'
        #).fetchall()
    
    #return(number_of_comments)

# https://www.kevin7.net/post_detail/tinymce-and-flask
#https://pypi.org/project/bleach/
#https://www.tiny.cloud/blog/bootstrap-wysiwyg-editor/
#https://www.tiny.cloud/docs/general-configuration-guide/upload-images/
# new post entry
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/post', methods=('GET', 'POST'))
@login_required
def post():
    if request.method == 'POST':
        
        clean = re.compile('<.*?>')

        title = request.form['title']
        body = re.sub(clean, '', request.form['body'])
        file = request.files['file']

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            post_image = 'upload/'+filename
            #path_1 = UPLOAD_FOLDER+filename
            
            if not body:
                body = "empthy"

            db = get_db()
            db.execute(
                'INSERT INTO post (post_title, post_body, author_id, post_image, comment)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, g.user['user_id'],  post_image, 0)
            )
            db.commit()
            return redirect("/")

        post_image = "empthy"
            
        db = get_db()
        db.execute(
            'INSERT INTO post (post_title, post_body, author_id, post_image, comment)'
            ' VALUES (?, ?, ?, ?, ?)',
            (title, body, g.user['user_id'], post_image, 0)
        )
        db.commit()
        return redirect("/")

    else:
        return render_template('blog/post.html')


def get_post(id):
    entry = get_db().execute(
        'SELECT p.post_id, post_title, post_body, post_created, author_id, username, post_image, comment'
        ' FROM post p JOIN user u ON p.author_id = u.user_id'
        ' WHERE p.post_id = ?',
        (id,)
    ).fetchone()

    if entry is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return entry


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    entry = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET post_title = ?, post_body = ?'
                ' WHERE post_id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=entry)

################################################################

#look into this
#https://stackoverflow.com/questions/52105439/adding-comments-to-a-flask-blog-webapp
@bp.route('/<int:id>/reply', methods=('GET', 'POST'))
@login_required
def reply(id):
    blog_post = get_post(id)
    print(blog_post)

    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
       

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO comments (commentor_id, OG_post_id, comment_body, comment_title)'
                ' VALUES (?, ?, ?, ?)',
                (g.user['user_id'] , id, body, title)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/reply.html', post=blog_post)

###################################################################

def get_comments(id):
    entry = get_db().execute(
        'SELECT *'
        ' FROM comments'
        ' WHERE post_id = ?',
        (id,)
    )

    if entry is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return entry

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE post_id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

# change password 
@bp.route("/PasswordChange", methods=["GET", "POST"])
@login_required
def PasswordChange():

    if request.method == 'POST':

        username = request.form['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        new_password_repeat = request.form['new_password_repeat']

        # all the checks
        if not username:
            error = 'Incorrect username'

        elif not old_password:
            error = 'Incorrect password.'
           
        elif not new_password:
            error = 'Needs a new password.'

        elif not new_password_repeat:
            error = 'Repeat the new password.'
           
        elif not check_password_hash(new_password, new_password_repeat):
             error = 'New password doesnt match.'
        
        # hash the new password
        new_storage =  generate_password_hash(request.form.get("new_password_repeat"))

        print(new_storage)
        print(new_password)

        #call the db for the user
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        print(user)

        # verify the input
        if len(user) != 1 or not check_password_hash(user["password"], old_password):
            error = "you have given incorrect data"

        # update the db
        db.execute('UPDATE user SET password = ? WHERE username = ? ', (new_storage, username))
        db.commit()
        
        return redirect(url_for('index'))  

    return render_template('blog/PasswordChange.html') 

