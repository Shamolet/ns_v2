from app.admin import adm
from flask import render_template

@adm.route('/admin', methods=['GET', 'POST'])
def admin_login():

    return render_template('admin/admin.html', title='Войти в админку')
