from saleapp import app, dao, admin, login, controllers


app.add_url_rule('/', 'index', controllers.index)
app.add_url_rule('/login-admin', 'login-form', controllers.login_form)
app.add_url_rule('/login-admin', 'login-admin', controllers.login_admin, methods=['post'])
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule('/login', 'login-user', controllers.login_my_user, methods=['get', 'post'])
app.add_url_rule('/register', 'register', controllers.register, methods=['get', 'post'])
app.add_url_rule('/register_patient','register_patient', controllers.register_patient)
app.add_url_rule('/patient/register','register_patient_form', controllers.add_patient, methods=['post'])



@login.user_loader
def load_user(account_id):
    return dao.get_account_by_id(account_id)

if __name__ == '__main__':
    app.run(debug=True)
