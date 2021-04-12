from flask import Blueprint, render_template, request, flash
from .models import Employee, Pay, Record
from . import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@views.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template("admin.html")


@views.route('/create-new-user', methods=['GET', 'POST'])
def create_new_user():
    if request.method == 'POST':
        try:
            employee_id = request.form.get('employeeId')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            pay_per_hour = request.form.get('payPerHour')

            employee = Employee.query.filter_by(EmployeeId=employee_id).first()
            if employee:
                flash('Employee ID already exists!', category='error')
            else:
                new_employee = Employee(EmployeeId=employee_id, FirstName=first_name, LastName=last_name)
                new_pay = Pay(PayPerHour=pay_per_hour, EmployeeId=employee_id)
                db.session.add(new_employee)
                db.session.add(new_pay)
                db.session.commit()
                flash('New user created!', category='success')
        except Exception as e:
            db.session.rollback()
            flash('Error in created new user', category='error')
            print(e)
    return render_template("create-new-user.html")


@views.route('/user', methods=['GET','POST'])
def user():
    if request.method == 'POST':
        try:
            employee_id = request.form.get('employeeId')
            date = request.form.get("clockIn")

            employee = Employee.query.filter_by(EmployeeId=employee_id).first()
            if employee != employee_id:
                flash('Did not find employee id!', category='error')
            else:
                new_record = Employee(EmployeeId=employee_id, Date=date, TimeInFlag=1)
                db.session.add(new_record)
                db.session.commit()
                flash('Clocked in!', category='success')
        except Exception as e:
            db.session.rollback()
            flash('Error in clocking in', category='error')
            print(e)
    return render_template("user.html")