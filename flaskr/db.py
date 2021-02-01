import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# connection to the db
def get_db():
    if 'db' not in g:
        # link to the database
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # tells connection to return rows that behave like rows, gives access to column names 
        g.db.row_factory = sqlite3.Row

    return g.db

# check to see if connection to db was established.
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# python function to run SQL commands
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    # tells Flask to call this function when cleaning up after returning the responce
    app.teardown_appcontext(close_db)
    # adds a new command that can be called with the flask command.
    app.cli.add_command(init_db_command)