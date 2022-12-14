from flask import render_template, request, redirect, session, jsonify
from saleapp import app, dao, db
from saleapp.models import AccountModel
from flask_login import login_user, logout_user
import cloudinary.uploader
from saleapp.decorator import anonymous_user

def index():
    return render_template('index.html')

def login_form():
    return render_template('login.html')

def load_account(account_id):
    return dao.get_account_by_id(account_id)


def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        account = dao.auth_account(username, password)
        if account and account.is_active == True:
            login_user(user=account)
    return redirect('/admin')

def get_role_name_by_role_id(role_id=None):
    return db.session.query(AccountModel.user_role) \
        .filter(AccountModel.role_id.__eq__(role_id)).first()[0]


def logout_my_user():
    logout_user()
    return redirect('/login')


def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            try:
                dao.register(name=request.form['name'],
                             password=password,
                             username=request.form['username'], avatar=avatar)

                return redirect('/login')
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)

def register_patient():
    return render_template('register_patient.html')

@anonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_account(username=username, password=password)
        if user:
            login_user(user=user)

            n = request.args.get('next')
            return redirect(n if n else '/')

    return render_template('login_user.html')

def add_patient():
    a = count_patient_rule()
    if (a < 40):
        try:
            patient = dao.save_patient(first_name=request.json['first_name'],
                                       last_name=request.json['last_name'],
                                       email=request.json['email'],
                                       phone_number=int(request.json['phone_number']),
                                       id_card=int(request.json['id_card_input']))
        except:
            db.session.rollback()
            return jsonify({'status': 500})
        else:
            return jsonify({'status': 204})
    else:
        return jsonify({'status': 100})

def count_patient_rule():
    patient = dao.load_patient_info()
    count = 0
    for a in patient:
        count = count + 1
    return count

def count_medicine_rule():
    medicine = dao.load_medicine()
    count = 0
    for me in medicine:
        count = count +1
    return count



