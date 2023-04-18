from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class ResultRepsForm(FlaskForm):
    result = IntegerField('Результат, количество повторений',
                          validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


# Разобраться с полями даты
class ResultTimeForm(FlaskForm):
    minutes = IntegerField('мин', validators=[DataRequired()])
    seconds = IntegerField('сек', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class ResultBooleanForm(FlaskForm):
    result = BooleanField('Результат, Done или Не Done?', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
