from flask import Blueprint, render_template, request, flash, jsonify
from .models import Employee, Pay, Record, EmployeeSchema, employee_schema, employees_schema, pay_schema, pays_schema, record_schema, records_schema
from . import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    return jsonify({"key":"value"})


@views.route('/postemployee', methods=['POST'])
def post_employee():
    first_name = request.json['FirstName']
    last_name = request.json['LastName']

    employee = Employee(first_name, last_name)
    db.session.add(employee)
    db.session.commit()
    return employee_schema.jsonify(employee)


@views.route('/getemployee', methods=['GET'])
def get_employee():
    all_employees = Employee.query.all()
    results = employees_schema.dump(all_employees)
    return jsonify(results)


@views.route('/postpay', methods=['POST'])
def post_pay():
    pay_per_hour = request.json['PayPerHour']
    employee_id = request.json['EmployeeId']

    pay = Pay(pay_per_hour, employee_id)
    db.session.add(pay)
    db.session.commit()
    return employee_schema.jsonify(pay)


@views.route('/getpay', methods=['GET'])
def get_pay():
    all_pays = Pay.query.all()
    results = pays_schema.dump(all_pays)
    return jsonify(results)


@views.route('/postrecord', methods=['POST'])
def post_record():
    clocked_in = request.json['ClockedIn']
    employee_id = request.json['EmployeeId']

    record = Record(clocked_in, employee_id)
    db.session.add(record)
    db.session.commit()
    return employee_schema.jsonify(record)


@views.route('/getrecord', methods=['GET'])
def get_record():
    all_records = Record.query.all()
    results = records_schema.dump(all_records)
    return jsonify(results)


# @views.route('/admin', methods=['GET', 'POST'])
# def admin():
#     return render_template("admin.html")


# @views.route('/create-new-user', methods=['GET', 'POST'])
# def create_new_user():
#     if request.method == 'POST':
#         try:
#             employee_id = request.form.get('employeeId')
#             first_name = request.form.get('firstName')
#             last_name = request.form.get('lastName')
#             pay_per_hour = request.form.get('payPerHour')

#             employee = Employee.query.filter_by(EmployeeId=employee_id).first()
#             if employee:
#                 flash('Employee ID already exists!', category='error')
#             else:
#                 new_employee = Employee(EmployeeId=employee_id, FirstName=first_name, LastName=last_name)
#                 new_pay = Pay(PayPerHour=pay_per_hour, EmployeeId=employee_id)
#                 db.session.add(new_employee)
#                 db.session.add(new_pay)
#                 db.session.commit()
#                 flash('New user created!', category='success')
#         except Exception as e:
#             db.session.rollback()
#             flash('Error in created new user', category='error')
#             print(e)
#     return render_template("create-new-user.html")


# @views.route('/user', methods=['GET','POST'])
# def user():
#     if request.method == 'POST':
#         try:
#             employee_id = request.form.get('employeeId')
#             clocked_in = request.form.get('clockIn')
#             print(clocked_in)
#             employee = Employee.query.filter_by(EmployeeId=employee_id).first()

#             if employee.EmployeeId != int(employee_id):
#                 flash('Did not find employee id!', category='error')
#             elif clocked_in == True:
#                 new_record = Record(EmployeeId=employee_id, Date=date, TimeInFlag=1)
#                 db.session.add(new_record)
#                 db.session.commit()
#                 flash('Clocked in!', category='success')
#             else:
#                 new_record = Record(EmployeeId=employee_id, Date=date, TimeInFlag=0)
#                 db.session.add(new_record)
#                 db.session.commit()
#                 flash('Clocked out!', category='success')
#         except Exception as e:
#             db.session.rollback()
#             flash('Error in clocking in/out', category='error')
#             print(e)
#     return render_template("user.html")