from flask_admin import AdminIndexView, BaseView, expose
from flask_sqlalchemy import SQLAlchemy
from app.models.user_models import User, Comment
from app import db



class AnyPageView(BaseView):
    @expose('/')
    def any_page(self):
        return self.render('admin/index.html')

class DashBoardView(AdminIndexView):
    @expose('/')
    def add_data_db(self):
        for i in range(10):
            if not len(User.query.all()) >= 10:
                user = User(username=person.full_name(), email=person.email(), password=person.password())
                db.session.add(user)
                db.session.commit()

                comment = Comment(username=user.username, body='Клевая статья. Всем добра', post_id=post.id)
                db.session.add(comment)
            db.session.commit()
        all_users = User.query.all()
        all_comments = Comment.query.all()
        return self.render('admin/dashboard_index.html', all_users=all_users, all_posts=all_posts,
                           all_comments=all_comments)
