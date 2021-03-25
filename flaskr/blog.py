from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, url_for, escape, current_app, send_from_directory
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db

import re
import os

from config import UPLOAD_FOLDER
from helpers import get_comments, number_of_comments, get_post, get_comment, allowed_file


bp = Blueprint('blog', __name__)

###### ROUTES ######
###### INDEX ######
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


###### LANDING PAGE ######
@bp.route('/post')
@login_required
def post():
    
    return render_template('blog/post_selection.html')

## Link from where i got ideas for implementation of the blog concept and TinyMCE.
# https://www.kevin7.net/post_detail/tinymce-and-flask
#https://pypi.org/project/bleach/
#https://www.tiny.cloud/blog/bootstrap-wysiwyg-editor/
#https://www.tiny.cloud/docs/general-configuration-guide/upload-images/
# new post entry
###### BLOG POST WITHOUT IMAGE ######
@bp.route('/title_body', methods=('GET', 'POST'))
@login_required
def title_body():
    if request.method == 'POST':

        clean = re.compile('<.*?>')

        title = request.form['title']
        body = re.sub(clean, '', request.form['body'])
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)

         # has to add this due to NOT NULL in db
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
        return render_template('blog/title_body.html')

###### BLOG POST WITH TITLE AND IMAGE ######
@bp.route('/title_image', methods=('GET', 'POST'))
@login_required
def title_image():
    if request.method == 'POST':


        title = request.form['title']
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
            
            # has to add this due to NOT NULL in db
            body = "empthy"

            db = get_db()
            # can remove cooment column from db
            db.execute(
                'INSERT INTO post (post_title, post_body, author_id, post_image)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['user_id'],  post_image)
            )
            db.commit()
            return redirect("/")

    else:
        return render_template('blog/title_image.html')

###### BLOG POST WITH TITLE, IMAGE AND TEXT ######
@bp.route('/title_image_text', methods=('GET', 'POST'))
@login_required
def title_image_text():
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

        # TODO I feel i am missing some erroor hooks over here....

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

    else:
        return render_template('blog/title_image_text.html')

###### EDIT/UPDATE POST ######

@bp.route('/<int:id>/update_post', methods=('GET', 'POST'))
@login_required
def update_post(id):
    entry = get_post(id)

    if request.method == 'POST':
        
        clean = re.compile('<.*?>')
        title = request.form['title']
        body = re.sub(clean, '', request.form['body'])
        file = request.files['file']

        if not file:
            db = get_db()
            db.execute(
                'UPDATE post SET post_title = ?, post_body = ? '
                ' WHERE post_id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

        file = request.files['file']

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        
        else:

            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            post_image = 'upload/'+filename
            db = get_db()
            db.execute(
                'UPDATE post SET post_title = ?, post_body = ?, post_image= ? '
                ' WHERE post_id = ?',
                (title, body, post_image, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update_post.html', post=entry)

###### EDIT/UPDATE COMMENT ######

@bp.route('/<int:id>/update_comment', methods=('GET', 'POST'))
@login_required
def update_comment(id):
    entry = get_comment(id)

    if request.method == 'POST':
        
        clean = re.compile('<.*?>')
        title = request.form['title']
        body = re.sub(clean, '', request.form['body'])
        post_id = request.form.get('post_id')

        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        
        else:

            db = get_db()
            db.execute(
                'UPDATE comments SET comment_title = ?, comment_body = ? '
                ' WHERE comment_id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.reply', id=post_id))

    return render_template('blog/update_comment.html', comment=entry)


###### COMMENT ON A POST ######
#I got help and inspiration from the following link
#https://stackoverflow.com/questions/52105439/adding-comments-to-a-flask-blog-webapp
@bp.route('/<int:id>/reply', methods=('GET', 'POST'))
@login_required
def reply(id):

    clean = re.compile('<.*?>')
    blog_post = get_post(id)
    comments = get_comments(id)

    if request.method == 'POST':

        title = request.form['title']
        body = re.sub(clean, '', request.form['body'])
        clean = re.compile('<.*?>')
        post_id = request.form.get('post_id')

        print('post_id') 
        print(post_id) 

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
            return redirect(url_for('blog.reply', id=post_id))

    return render_template('blog/reply.html', post=blog_post, comments=comments)


###### DELETE POST ######
@bp.route('/<int:id>/delete_post', methods=('POST',))
@login_required
def delete_post(id):
    get_post(id)
    db = get_db()
    
    db.execute('DELETE FROM post WHERE post_id = ?', (id,))
    db.commit()

    db.execute('DELETE FROM comments WHERE OG_post_id = ?', (id,))
    db.commit()

    flash ('Post deleted')
    return redirect(url_for('blog.index'))

###### DELETE COMMENT ######
@bp.route('/<int:id>/delete_comment', methods=('POST',))
@login_required
def delete_comment(id):

    comment = get_comment(id)

    db = get_db()

    post_id = get_db().execute(
        'SELECT OG_post_id'
        ' FROM comments'
        ' WHERE comment_id = ?',
        (id,)
    ).fetchone()
   
    db.execute('DELETE FROM comments WHERE comment_id = ?', (id,))
    
    db.commit()
        
    flash ('Comment deleted')
    return redirect(url_for('blog.reply', id=post_id[0]))
    

