from flask_script import Manager

from app import create_app, db
from app.models import User, Comment, Exercise, WOD, Result

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)
manager.add_command('init_db', InitDbCommand)
manager.run(debug=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'users': User, 'comments': Comment, 'exercises': Exercise,
            'wods': WOD, 'results': Result}