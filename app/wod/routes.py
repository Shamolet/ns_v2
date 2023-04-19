from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.forms.forms import CommentForm
from app.forms.result_forms import ResultBoolForm, ResultTimeForm, ResultRepsForm
from app.models.models import WOD, ResultRep, Comment, ResultBool
from app.wod import wod_bp


# Block WODs
@wod_bp.route('/wods')
def wods():
    wods_list = WOD.query.order_by(WOD.date_posted.desc()).all()
    return render_template('main/wods_list.html',
                           wods_list=wods_list, title='Список тренировок')


@wod_bp.route('/wods/<int:id>', methods=['GET', 'POST'])
@login_required
def wod_detail(id):
    detail = WOD.query.get(id)

    # Reps

    if detail.type_result == 1:
        result_rep_form = ResultRepsForm()
        if result_rep_form.validate_on_submit():
            result = ResultRep(result=result_rep_form.result.data,
                                author_result_rep=current_user, wod_result_rep=detail)
            db.session.add(result)
            db.session.commit()
            flash('Результат сохранен!')
            return redirect(url_for('wod_bp.wod_detail', id=id))

        results = ResultRep.query.filter_by(wod_id=id). \
            filter_by(author_result_rep=current_user). \
            order_by(ResultRep.date_posted.desc()).first()

        return render_template('main/wod_detail.html', detail=detail,
                               result_rep_form=result_rep_form,
                               results=results)

    else:
        result_bool_form = ResultBoolForm()
        if result_bool_form.validate_on_submit():
            result = ResultBool(confirm=result_bool_form.result.data,
                                author_result_bool=current_user, wod_result_bool=detail)
            db.session.add(result)
            db.session.commit()
            flash('Поздравляем с выполнением тренировки!')
            return redirect(url_for('wod_bp.wod_detail',
                                    result_bool_form=result_bool_form, id=id))

        results = ResultBool.query.filter_by(wod_id=id). \
            filter_by(author_result_bool=current_user). \
            order_by(ResultBool.date_posted.desc()).first()

        return render_template('main/wod_detail.html', detail=detail,
                               result_bool_form=result_bool_form,
                               results=results)

    # elif detail.type_result == 2:
    #     result_time_form = ResultTimeForm()
    #
    #
    # elif detail.type_result == 3:
    #     result_time_form = ResultTimeForm()
    #     result_rep_form = ResultRepsForm()
    #
    #

    result_time_form = ResultTimeForm()

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(body=comment_form.comment.data,
                          author_comment=current_user, wod_comment=detail)
        db.session.add(comment)
        db.session.commit()
        flash('Коммент опубликован!')
        return redirect(url_for('main.wod_detail', id=id))
    comments = Comment.query.filter_by(wod_id=id).\
        order_by(Comment.timestamp.desc()).all()
    return render_template('main/wod_detail.html', comments=comments,
                           detail=detail, comment_form=comment_form,
                           result_time_form=result_time_form,
                           results=results)
