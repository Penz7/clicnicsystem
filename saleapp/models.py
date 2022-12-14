from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from saleapp import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime, date
import hashlib


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    DOCTOR = 3
    NURSE = 4
    CASHIER = 5


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class AccountModel(BaseModel, UserMixin):
    __tablename__ = 'account_model'

    first_name = Column(String(20), default='')
    last_name = Column(String(50), default='')
    email = Column(String(50), default='')
    phone_number = Column(String(10), default='')
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    medical_bill_list = relationship('MedicalBillModel', backref='account', lazy=True)
    medical_examination = relationship('MedicalExaminationModel', backref='account', lazy=True)




class PatientModel(BaseModel):
    __tablename__ = 'patient_model'

    date_created = Column(DateTime, default=date.today())
    first_name = Column(String(20), default='')
    last_name = Column(String(50), default='')
    email = Column(String(50), default='')
    phone_number = Column(String(10), default='')
    id_card = Column(Integer, unique=True, nullable=False)
    # relationship

    medical_examination = relationship('MedicalExaminationModel', backref='patient', lazy=True)



class MedicineModel(BaseModel):
    __tablename__ = 'medicine_model'
    # attributes
    name = Column(String(100), unique=True, default='', nullable=False)
    unit_price = Column(Integer, default=0.0)
    import_date = Column(DateTime, default=datetime.now())
    expiration_date = Column(DateTime, default=datetime.now())
    description = Column(String(200), default='')
    medicine_detail = relationship('MedicineExaminationDetailModel', backref='medicine' , lazy=True)
    medicine_unit_id = Column(Integer, ForeignKey('medicine_unit_model.id'), nullable=False)

    def __str__(self):
        return self.name

class MedicineUnitModel(BaseModel):
    __tablename__ = 'medicine_unit_model'

    # attribute
    name = Column(String(30), nullable=False, unique=True, default='')

    # relationship
    medicine_list = relationship('MedicineModel', backref='medicine_unit', lazy=True)

    def __str__(self):
        return self.name

class MedicineExaminationDetailModel(BaseModel):
    __tablename__ = 'medical_examination_detail_model'

    amount = Column(Integer, default=0)
    dosage = Column(String(200), default='')
    using_method = Column(String(200), default='')

    medicine_id = Column(Integer, ForeignKey('medicine_model.id'), nullable=False)

    medical_examination_id = Column(Integer, ForeignKey('medical_examination_model.id'), nullable=False)

class MedicalExaminationModel(BaseModel):
    __tablename__ = 'medical_examination_model'

    # attributed
    date_created = Column(DateTime, default=datetime.now())
    symptom = Column(String(200), default='')
    predicted_disease = Column(String(200), default='')
    medical_examination_id = Column(Integer, unique=True, nullable=False)

    # foreign keys
    medical_bill = relationship('MedicalBillModel',backref='medical_examination', uselist=False, lazy=True)

    account_id = Column(Integer, ForeignKey('account_model.id'), nullable=False)

    patient_id = Column(Integer, ForeignKey('patient_model.id'), nullable=False)

    medical_detail = relationship('MedicineExaminationDetailModel', backref='medical_examination', lazy=True)



class MedicalBillModel(BaseModel):
    __tablename__ = 'medical_bill_model'

    # attribute
    created_date = Column(DateTime, default=datetime.now())
    medical_price = Column(Integer, default=0)
    medical_examination_price = Column(Integer, default=0)
    total_price = Column(Integer, default=0)

    # foreign key
    account_id = Column(Integer, ForeignKey('account_model.id'), nullable=False)
    medical_examination_id = Column(Integer, ForeignKey('medical_examination_model.id'),  nullable=False)

class RuleModel(BaseModel):
    __tablename__ = 'rule_model'

    # attribute
    name = Column(String(150), unique=True, nullable=False, default='')
    amount = Column(Integer, default=0)

    def __str__(self):
        return self.name

class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # a = AccountModel(username='dat', password=password, user_role='USER',
        #           avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        # db.session.add(a)
        # db.session.commit()

        # user = PatientModel(first_name='fdgfdgdfg', last_name='cap', email='dat@gmail.com', phone_number=1123124, id_card=654645654)
        # db.session.add(user)
        # db.session.commit()

        # c1 = Category(name='Trang chủ')
        # c2 = Category(name='Thông tin')
        # c3 = Category(name='Chất lượng')
        # c4 = Category(name='Liên hệ')
        # c5 = Category(name='Phản hồi')
        #
        # db.session.add_all([c1, c2, c3, c4, c5])
        # db.session.commit()

        # c1 = MedicineUnitModel(name='Viên tổng hợp')
        # c2 = MedicineUnitModel(name='Viên nén')
        #
        # db.session.add_all([c1, c2])
        # db.session.commit()
        #
        # p1 = MedicineModel(name='A', unit_price=18000, description='Thuốc ho', medicine_unit_id=1)
        # p2 = MedicineModel(name='B', unit_price=15000, description='Thuốc đau bụng', medicine_unit_id=2)
        # p3 = MedicineModel(name='C', unit_price=58000, description='Thuốc tiêu chảy', medicine_unit_id=1)
        # p4 = MedicineModel(name='D', unit_price=108000, description='Thuốc đau đầu', medicine_unit_id=2)
        # db.session.add_all([p1,p2,p3,p4])
        # db.session.commit()

        # m = MedicalBillModel(medical_price=int('10000'),
        #                                 medical_examination_price=int('20000'),
        #                                 total_price=int('20000'),
        #                                 account_id=2,
        #                                 medical_examination_id=7)
        # db.session.add(m)
        # db.session.commit()
