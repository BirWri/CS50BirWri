from flaskr.db import get_db
from flask import Response

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def number_of_comments(post_id):

    db = get_db()
    number_of_comments = db.execute(
            'SELECT COUNT (OG_post_id)'
            ' FROM comments'
            ' WHERE OG_post_id = ?',
            (post_id,)
    )

    #https://stackoverflow.com/questions/47716237/python-list-how-to-remove-parenthesis-quotes-and-commas-in-my-list
    # to make the program actually display the int and not show the parenthesis
    number_of_comments = [i[0] for i in number_of_comments]
    
    #https://stackoverflow.com/questions/13207697/how-to-remove-square-brackets-from-list-in-python
    # trying to remove the []
    number_of_comments = str(number_of_comments)[1:-1]
    
    return(number_of_comments)


def get_comments(id):
    entry = get_db().execute(
        'SELECT *'
        ' FROM comments JOIN user ON commentor_id = user_id'
        ' WHERE OG_post_id = ?',
        (id,)
    )

    if entry is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return entry


def get_post(id):
    entry = get_db().execute(
        'SELECT p.post_id, post_title, post_body, post_created, author_id, username, post_image'
        ' FROM post p JOIN user u ON p.author_id = u.user_id'
        ' WHERE p.post_id = ?',
        (id,)
    ).fetchone()

    if entry is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return entry


def get_comment(id):
    entry = get_db().execute(
        'SELECT *'
        ' FROM comments'
        ' WHERE comment_id = ?',
        (id,)
    ).fetchone()


    if entry is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return entry


def get_image(cartoon_title):
    entry = get_db().execute(
        'SELECT *'
        ' FROM cartoon'
        ' WHERE cartoon_title = ?',
        (cartoon_title,)
    ).fetchone()

    if entry is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    return (entry)