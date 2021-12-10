from . import db, ma
from sqlalchemy.sql import func
from datetime import datetime


class Employee(db.Model):
    __tablename__ = 'Employee'
    EmployeeId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(20))
    LastName = db.Column(db.String(20))

    def __init__(self, FirstName, LastName):
        self.FirstName = FirstName
        self.LastName = LastName


class Pay(db.Model):
    __tablename__ = 'Pay'
    PayId = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, default = datetime.now)
    PayPerHour = db.Column(db.Integer)
    EmployeeId = db.Column(db.Integer, db.ForeignKey('Employee.EmployeeId'))

    def __init__(self, PayPerHour, EmployeeId):
        self.PayPerHour = PayPerHour
        self.EmployeeId = EmployeeId


class Record(db.Model):
    __tablename__ = 'Record'
    RecordId = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, default = datetime.now)
    ClockedIn = db.Column(db.Boolean)
    EmployeeId = db.Column(db.Integer, db.ForeignKey('Employee.EmployeeId'))

    def __init__(self, ClockedIn, EmployeeId):
        self.ClockedIn = ClockedIn
        self.EmployeeId = EmployeeId


class EmployeeSchema(ma.SQLAlchemySchema):
    """Defines a marshmallow schema for employee data that is passed to/from frontend and backend"""
    class Meta:
        fields = ('EmployeeId', 'FirstName', 'LastName')


class PaySchema(ma.SQLAlchemySchema):
    """Defines a marshmallow schema for employee data that is passed to/from frontend and backend"""
    class Meta:
        include_fk = True
        fields = ('PayId', 'Date', 'PayPerHour', 'EmployeeId')


class RecordSchema(ma.SQLAlchemySchema):
    """Defines a marshmallow schema for employee data that is passed to/from frontend and backend"""
    class Meta:
        include_fk = True
        fields = ('RecordId', 'Date', 'ClockedIn', 'EmployeeId')


# Creates object of the employee schema
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

# Creates object of the pay schema
pay_schema = PaySchema()
pays_schema = PaySchema(many=True)

# Creates object of the record schema
record_schema = RecordSchema()
records_schema = RecordSchema(many=True)