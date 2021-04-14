from . import db
from sqlalchemy.sql import func
from datetime import datetime


class Employee(db.Model):
    __tablename__ = 'Employee'
    EmployeeId = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(20))
    LastName = db.Column(db.String(20))


class Pay(db.Model):
    __tablename__ = 'Pay'
    PayId = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, default=func.now())
    PayPerHour = db.Column(db.Integer)
    EmployeeId = db.Column(db.Integer, db.ForeignKey('Employee.EmployeeId'))


class Record(db.Model):
    __tablename__ = 'Record'
    RecordId = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, default=func.now())
    TimeInFlag = db.Column(db.Integer)
    EmployeeId = db.Column(db.Integer, db.ForeignKey('Employee.EmployeeId'))