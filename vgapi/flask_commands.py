from vgapi import APP, DB

def reset_db():
    import models
    DB.drop_all()
    DB.create_all()


def init_db():
    """ Sets up a test DB """
    with APP.open_resource('schema.sql', mode='r') as f:
        lines = f.read()
        DB.engine.execute(lines)

    DB.create_all()


@APP.cli.command('initdb')
def initdb_command():
    """ Sets up shell command for initializing the DB """
    init_db()
    print('Initialized the DB')


@APP.cli.command('resetdb')
def resetdb_command():
    reset_db()
    print('Reset the DB')
