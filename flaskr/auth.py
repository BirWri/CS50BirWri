import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from functools import wraps

from wtforms import Form, BooleanField, StringField, PasswordField, validators



bp = Blueprint('auth', __name__, url_prefix='/auth')

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        print(username)
        print(password)

        db = get_db()

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            flash('Thank you for registering')
            return redirect(url_for('auth.login'))

        flash(error)
      
    return render_template('auth/register.html', form=form)

# register new user
#@bp.route('/register', methods=('GET', 'POST'))
#def register():
    #if request.method == 'POST':
       # username = request.form['username']
       # password = request.form['password']
       # password2 = request.form['password2']

       # db = get_db()
       # error = None

       # if not username:
       #     error = 'Username is required.'
       # elif not password:
        #    error = 'Password is required.'
        #elif db.execute(
        #    'SELECT user_id FROM user WHERE username = ?', (username,)
        #).fetchone() is not None:
        #    error = 'User {} is already registered.'.format(username)
        #elif password != password2:
       #     error = 'Passwords did not match.'

        #if error is None:
         #   db.execute(
         #       'INSERT INTO user (username, password) VALUES (?, ?)',
          #      (username, generate_password_hash(password))
          #  )
          #  db.commit()
          #  return redirect(url_for('auth.login'))

        #flash(error)

    #return render_template('auth/register.html')


# login form
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username/password.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username/password.'

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# at the beginning of each request, if a user is logged in their information
# should be loaded and made available to other views.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE user_id = ?', (user_id,)
        ).fetchone()        


# log out
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# require authetication in other views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
