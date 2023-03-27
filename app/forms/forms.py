from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length


class EditProfileForm(FlaskForm):
    username = StringField('Никнейм', validators=[DataRequired()])

    about_me = TextAreaField('Обо мне',
                             validators=[Length(min=0, max=140)])
    bith = DateField('Дата рождения', format='%Y-%m-%d', validators=[DataRequired()])

    submit = SubmitField('Тык')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username


class EmptyForm(FlaskForm):
    submit = SubmitField('Тык')


class CommentForm(FlaskForm):
    comment = TextAreaField('Черкни что-нибудь', validators=[DataRequired()])
    submit = SubmitField('Тык')


class ResultForm(FlaskForm):
    result = StringField('Результат', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
