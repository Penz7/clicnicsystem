from operator import and_
from saleapp.models import Category,PatientModel, RuleModel, AccountModel, MedicineModel, MedicalExaminationModel, MedicalBillModel,MedicineExaminationDetailModel
from saleapp import db
from flask_login import current_user
from sqlalchemy import func, extract
import hashlib

def load_medicine():
    return MedicineModel.query.all()

def load_medicine_examination():
    return MedicalExaminationModel.query.all()

def load_categories():
    return Category.query.all()

def load_patient_info():
    return PatientModel.query.all()

def load_account_info():
    return AccountModel.query.all()

def auth_account(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return AccountModel.query.filter(AccountModel.username.__eq__(username.strip()),
                             AccountModel.password.__eq__(password)).first()

def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    a = AccountModel(first_name=name, username=username.strip(), password=password, avatar=avatar)
    db.session.add(a)
    db.session.commit()

def get_account_by_id(account_id):
    return AccountModel.query.get(account_id)

def save_medicine_examination(symptom,predicted_disease, patient_id, medical_examination_id):
    medicine_model = MedicalExaminationModel(symptom=symptom,
                                             predicted_disease=predicted_disease,
                                             patient_id=patient_id,
                                             medical_examination_id=medical_examination_id,
                                             account=current_user)
    db.session.add(medicine_model)
    db.session.commit()

    return medicine_model

def save_medicine_examination_detail(amount,dosage, using_method, medicine_id, medical_examination_id):
    medicine_model_detail = MedicineExaminationDetailModel(amount=amount,
                                                           dosage=dosage,
                                                           using_method=using_method,
                                                           medicine_id=medicine_id,
                                                           medical_examination_id=medical_examination_id)
    db.session.add(medicine_model_detail)
    db.session.commit()
    return medicine_model_detail

def get_medicine_examination_id(id):
    return MedicalExaminationModel.query.get(id)

def get_medicine_examination_detail(id):
    return MedicineExaminationDetailModel.query.filter(MedicineExaminationDetailModel.medical_examination_id.__eq__(id)).all()



def get_rule_info():
    return RuleModel.query.all()

def get_rule_amount_medical(id):
    return RuleModel.query.get(id)

def get_medicical_examination_bill(id):
    return MedicalBillModel.query.get(id)

def get_medicine_bill_examinate_id(id):
    return MedicalBillModel.query.filter(MedicalBillModel.medical_examination_id.__eq__(id)).all()

def save_medicine_examination_bill(medical_price,medical_examination_price, total_price,account_id, medical_examination_id):
    medicine_bill = MedicalBillModel(medical_price=medical_price,
                                        medical_examination_price=medical_examination_price,
                                        total_price=total_price,
                                        account_id=account_id,
                                        medical_examination_id=medical_examination_id)
    db.session.add(medicine_bill)
    db.session.commit()
    return medicine_bill

def save_patient(first_name, last_name, email, phone_number, id_card):
    patient = PatientModel(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, id_card=id_card)
    db.session.add(patient)
    db.session.commit()
    return patient


# thống kê doanh thu theo từng tháng
def statistic_revenue_month(from_month=None, to_month=None):
    data = db.session.query(func.month(MedicalBillModel.created_date),
                            func.sum(MedicalBillModel.medical_price +
                                     MedicalBillModel.medical_examination_price)) \
        .group_by(func.month(MedicalBillModel.created_date)) \
        .order_by(func.month(MedicalBillModel.created_date))

    if from_month and to_month:
        data = data.filter(and_(extract('month', MedicalBillModel.created_date) >= extract('month',from_month),
                                extract('month', MedicalBillModel.created_date) <= extract('month', to_month)))
    return data.all()

# thống kê tần suất sử dụng thuốc theo tháng
def statistic_medicine_using_frequency_month(from_month=None, to_month=None, keyword=None):
    data = db.session.query(func.month(MedicalExaminationModel.date_created),
                            func.sum(MedicineExaminationDetailModel.amount)) \
        .join(MedicalExaminationModel) \
        .filter(MedicalExaminationModel.id == MedicineExaminationDetailModel.medical_examination_id) \
        .join(MedicineModel) \
        .filter(MedicineModel.id == MedicineExaminationDetailModel.medicine_id) \
        .group_by(func.month(MedicalExaminationModel.date_created)) \
        .order_by(func.month(MedicalExaminationModel.date_created))

    if keyword:
        data = data.filter(MedicineModel.name.__eq__(keyword))

    if from_month and to_month:
        data = data.filter(and_(extract('month', MedicalExaminationModel.date_created) >= extract('month',from_month),
                                extract('month', MedicalExaminationModel.date_created) <= extract('month', to_month)))
    return data.all()

# thống kê tần suất khám theo tháng
def statistic_medical_examination_month(from_month=None, to_month=None):
    data = db.session.query(func.month(MedicalExaminationModel.date_created),
                            func.count(MedicalExaminationModel.id)) \
        .group_by(func.month(MedicalExaminationModel.date_created)) \
        .order_by(func.month(MedicalExaminationModel.date_created))

    if from_month and to_month:
        data = data.filter(and_(func.month(MedicalExaminationModel.date_created) >= extract('month',from_month),
                                func.month(MedicalExaminationModel.date_created) <= extract('month', to_month)))
    return data.all()

