from app import create_app, db
from app.models.models import User, Comment, Exercise, WOD, Result

app = create_app()
app.run(debug=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'users': User, 'comments': Comment, 'exercises': Exercise,
            'wods': WOD, 'results': Result}
