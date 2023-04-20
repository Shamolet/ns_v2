from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange


class ResultRepsForm(FlaskForm):
    result = IntegerField('Результат, количество повторений',
                          validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


# Разобраться с полями даты
class ResultTimeForm(FlaskForm):
    minutes = IntegerField('мин', validators=[NumberRange(min=0)])
    seconds = IntegerField('сек', validators=[NumberRange(min=0, max=59)],
                           description='секунды от 0 до 59')
    submit = SubmitField('Подтвердить')


class ResultBoolForm(FlaskForm):
    result = BooleanField('Результат, True или Не True?', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
