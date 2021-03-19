import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from functools import wraps

from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField

from extensions import csrf

from forms import ChangePasswordForm,  RegistrationForm, LoginForm


bp = Blueprint('auth', __name__, url_prefix='/auth')


##### FUNCTIONS ######
# require authetication in other views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


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


##### ROUTES ######
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    
    
    if request.method == 'POST' and form.validate():

        username = form.username.data
        password = form.password.data

        db = get_db()
        db.execute(
            'INSERT INTO user (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
        flash('Thank you for registering')
        return redirect(url_for('auth.login'))
      
    return render_template('auth/register.html', form=form)



# login form
@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        
        username = form.username.data
        password = form.password.data
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

    return render_template('auth/login.html', form=form)


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

###### CHANGE PASSWORD ###### 
@bp.route("/PasswordChange", methods=["GET", "POST"])
@login_required
def PasswordChange():

    form = ChangePasswordForm(request.form)

    if request.method == 'POST':

        username = form.username.data
        old_password = form.old_password.data
        new_password = form.new_password.data
        confirm = form.confirm.data
        

        # all the checks
        if old_password == new_password:
            error = 'Old password cannot be the same as the new password'
            flash(error)
            return render_template('blog/PasswordChange.html', form=form) 
           
        if new_password != confirm:
            error = 'Confirm new password'
            flash(error)
            return render_template('blog/PasswordChange.html', form=form) 

        
        # hash the new password
        new_storage =  generate_password_hash(confirm)

        #call the db for the user
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # verify the input
        if user == None or not check_password_hash(user["password"], old_password):
            error = "Incorrect username/old password"
            flash(error)
            return render_template('blog/PasswordChange.html', form=form) 


        # update the db
        db.execute('UPDATE user SET password = ? WHERE username = ? ', (new_storage, username))
        db.commit()
        
        flash("You have successfully changed your password")
        return redirect(url_for('index'))  

    return render_template('blog/PasswordChange.html', form=form) 

# log out
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

