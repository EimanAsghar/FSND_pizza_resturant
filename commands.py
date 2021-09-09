import click
from flask.cli import with_appcontext

from models import (
    db,
    setup_db,
    db_drop_and_create_all,
    user,
    order,
    pizza
)

@click.command(name='create_tables')
@with_appcontext
def create_table():
    db.create_all()