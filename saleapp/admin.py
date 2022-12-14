from saleapp import db, app, dao
from saleapp.models import MedicineModel, MedicalBillModel, MedicalExaminationModel,UserRole, RuleModel, AccountModel
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import render_template
from flask_login import logout_user, current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea

from flask import request, jsonify, session



class AuthenticatedModelView(ModelView):
    column_hide_backrefs = False
    can_create = True
    can_edit = True
    can_delete = True
    create_modal = True
    edit_modal = True
    details_modal = True
    column_display_pk = True
    page_size = 10
    column_display_all_relations = True
    can_view_details = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')

        return super().__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class MedicineView(AuthenticatedModelView):
    # columns
    column_searchable_list = ['name', 'description']
    column_filters = ['name','unit_price']
    can_view_details = True
    column_exclude_list = ['image', 'description']
    can_export = True
    form_excluded_columns = ['medicine_detail']
    column_export_list = ['id', 'name', 'unit_price', 'import_date','expiration_date','description']
    column_labels = {
        'name': 'Tên thuốc',
        'unit_price': 'Đơn giá',
        'import_date': 'Ngày nhập kho',
        'expiration_date': 'Ngày hết hạn',
        'description': 'Mô tả'
    }
    page_size = 5
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }

class DoctorView(BaseView):
    @expose('/')
    def index(self):
        medicine = dao.load_medicine()
        patient = dao.load_patient_info()
        account = dao.load_account_info()
        medical_examination = dao.load_medicine_examination()
        return self.render('admin/doctor.html', medicine=medicine, patient=patient, account=account, medical_examination=medical_examination)

    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.DOCTOR


@app.route('/api/doctor/save_medical_examination_data', methods=['post'])
def save_medicine_examination():
    try:
        medicine_model = dao.save_medicine_examination(symptom=request.json['symptom'],
                                                        predicted_disease=request.json['predicted_disease'],
                                                        patient_id=int(request.json['patient_id_card']),
                                                        medical_examination_id=int(request.json['medical_examination_id']))
    except:
        db.session.rollback()
        return jsonify({'status': 500})
    else:
        return jsonify({'status': 204})

@app.route('/api/doctor/save_medical_examination_detail_data', methods=['post'])
def save_medicine_detail_examination():
    try:
        medicine_list = request.json['medicine_list']
        medical_examination_id = int(request.json['medical_examination_detail_id'])
        for medicine in medicine_list:
            medicine_model_detail = dao.save_medicine_examination_detail(amount=int(medicine['amount']),
                                                                     dosage=medicine['dosage'],
                                                                     using_method=medicine['using_method'],
                                                                     medicine_id=int(medicine['medicine_name_id']),
                                                                     medical_examination_id=medical_examination_id)


    except:
        db.session.rollback()
        return jsonify({'status': 500})
    else:
        return jsonify({
            'status': 204
        })


class NurseView(BaseView):
    @expose('/')
    def index(self):
        patient = dao.load_patient_info()
        return self.render('admin/nurse.html', patient=patient)

    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.NURSE

@app.route('/api/nurse/patient')
def patient():
    data = []
    for c in dao.load_patient_info():
        data.append({
            "first_name": c.first_name,
            "last_name": c.last_name,
            "date_create": c.date_created,
            "email": c.email,
            "phone_number": str(c.phone_number),
            "id_card": str(c.id_card)
        })

    return jsonify(data)

@app.route('/api/nurse/add_patient', methods=['post'])
def add_patient():
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


class CashierView(BaseView):
    @expose('/')
    def index(self):
        patient = dao.load_patient_info()
        rule = dao.get_rule_info()
        return self.render('admin/cashier.html', patient=patient, rule=rule)

    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.CASHIER

@app.route('/api/pay/load_patient_info', methods=['post'])
def medicine_price_total():
    try:
        data = []
        medicine_data = []
        total_price = 0
        medical_examination_id = int(request.json['medical_examination_id'])
        medical_examination = dao.get_medicine_examination_id(medical_examination_id)
        medical_detail = dao.get_medicine_examination_detail(medical_examination_id)
        data.append({
                'first_name_patient': medical_examination.patient.first_name,
                'last_name_patient': medical_examination.patient.last_name,
                'id_card_patient': str(medical_examination.patient.id_card),
                'medical_examination_id': str(medical_examination.medical_examination_id),
                'data_created': str(medical_examination.date_created),
                'predicted_disease': medical_examination.predicted_disease

        })
        for p in medical_detail:
            medicine_data.append({
                    'medicine_name': p.medicine.name,
                    'medicine_unit': p.medicine.medicine_unit.name,
                    'medicine_amount': str(p.amount),
                    'medicine_price': str(p.medicine.unit_price),
                    'total': str(p.amount*p.medicine.unit_price)
            })
            total_price+=p.amount*p.medicine.unit_price

    except:
        return jsonify({'status': 500})
    else:
        return jsonify(data,medicine_data,total_price)

@app.route('/api/cashier/save_medical_examination_bill', methods=['post'])
def save_medical_examination_bill():
    try:
        medical_examination_id = int(request.json['medical_examination_id'])
        medicine_bill = dao.save_medicine_examination_bill(medical_price=int(request.json['medical_price']),
                                        medical_examination_price=int(request.json['medical_examination_price_pay']),
                                        total_price=int(request.json['total_price']),
                                        account_id=int(request.json['account_id_current']),
                                        medical_examination_id=medical_examination_id)
    except:

        return jsonify({'status': 500})
    else:
        return jsonify({'status': 204})



class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = dao.statistic_revenue_month(from_month=request.args.get('from_month'),
                                          to_month=request.args.get('to_month'))

        return self.render('admin/stats_turnover.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated and \
               current_user.user_role == UserRole.ADMIN

class StatsExaminationView(AuthenticatedView):
        @expose('/')
        def index(self):
            stats_examination = dao.statistic_medical_examination_month(from_month=request.args.get('from_month'), \
                                                                        to_month=request.args.get('to_month'))

            return self.render('admin/stats_examination_medical.html',stats_examination=stats_examination)

        def is_accessible(self):
                return current_user.is_authenticated and \
                       current_user.user_role == UserRole.ADMIN

class StatsMedicineView(AuthenticatedView):
        @expose('/')
        def index(self):
            stats_medicine = dao.statistic_medicine_using_frequency_month(from_month=request.args.get('from_month'), \
                                                                          to_month=request.args.get('to_month'), \
                                                                          keyword=request.args.get('kw'))
            return self.render('admin/stats_medicine.html',stats_medicine=stats_medicine)

        def is_accessible(self):
                return current_user.is_authenticated and \
                       current_user.user_role == UserRole.ADMIN


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return render_template('login.html')


class AdminView(AdminIndexView):
    def is_visible(self):
        return not current_user.is_authenticated

    @expose('/')
    def index(self):
        return self.render('/admin/home_page.html')


admin = Admin(app=app, name='Quản trị viên', template_mode='bootstrap4', index_view=AdminView())
admin.add_view(AuthenticatedModelView(AccountModel, db.session, name='Quản lý tài khoản'))
admin.add_view(MedicineView(MedicineModel, db.session, name='Kho thuốc'))
admin.add_view(AuthenticatedModelView(MedicalExaminationModel, db.session, name='Phiếu khám'))
admin.add_view(AuthenticatedModelView(MedicalBillModel, db.session, name='Hóa đơn'))
admin.add_view(AuthenticatedModelView(RuleModel, db.session, name='Quy định'))
admin.add_view(DoctorView(name='Giao diện bác sĩ'))
admin.add_view(CashierView(name='Giao diện thu ngân'))
admin.add_view(NurseView(name='Giao diện y tá'))
admin.add_view(StatsView(name='Thống kê doanh thu'))
admin.add_view(StatsMedicineView(name='Thống kê thuốc'))
admin.add_view(StatsExaminationView(name='Thống kê khám'))
admin.add_view(LogoutView(name='Đăng xuất'))
