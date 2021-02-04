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


bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    if g.user is None:
        return render_template('blog/about.html')
    else: 
        db = get_db()
        posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY created DESC'
        ).fetchall()
        return render_template('blog/index.html', posts=posts)

#https://www.kevin7.net/post_detail/tinymce-and-flask
#https://pypi.org/project/bleach/
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        
        # To remove html tags from string
        #https://medium.com/@jorlugaqui/how-to-strip-html-tags-from-a-string-in-python-7cb81a2bbf44
        clean = re.compile('<.*?>')

        title = request.form['title']
        body = re.sub(clean, '', request.form['body'])
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            path_1 ="empthy"
            db.execute(
                'INSERT INTO post (title, body, author_id, path_1)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], path_1)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/post.html')

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

        print(file.filename)


        print(body)
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

        if not body:
            error = 'Content is required.'


        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            path_1 = UPLOAD_FOLDER+filename
            print(path_1)
            
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, path_1)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'],  path_1)
            )
            db.commit()
            return redirect("/")

        path_1 = "empthy"
        print(path_1)
            
        db = get_db()
        db.execute(
            'INSERT INTO post (title, body, author_id, path_1)'
            ' VALUES (?, ?, ?, ?)',
            (title, body, g.user['id'],  path_1)
        )
        db.commit()
        return redirect("/")

    else:
        return render_template('blog/post.html')

#potentsially not imoratnt function
@bp.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def get_post(id, check_author=True):
    entry = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if entry is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and entry['author_id'] != g.user['id']:
        abort(403)

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
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=entry)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
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

