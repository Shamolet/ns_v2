from flask_admin import AdminIndexView, BaseView, expose

# Define the Page View model.
class AnyPageView(BaseView):
    @expose('/')
    def any_page(self):
        return self.render('admin/admin.html')


# Define the Dash Board view model.
class DashBoardView(AdminIndexView):
    @expose('/')
    def add_data_db(self):
        return self.render('admin/dashboard_index.html')
