# importing essential libs
from enum import unique
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import false
from sqlalchemy import text

app = Flask(__name__, template_folder='templates')

# setup the database uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@localhost/emp_dpt_db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# database connector
db = SQLAlchemy(app)

# creating EmployeeDepartment Table

empdpt = db.Table('EmployeeDepartments',
    db.Column('id',db.Integer, primary_key=True),
    db.Column('empId',db.Integer, db.ForeignKey('Employee.Id')),
    db.Column('dptId',db.Integer, db.ForeignKey('Department.Id'))
)



# creating employee model
class Employee(db.Model):
    __tablename__ = 'Employee'
    Id = db.Column(db.Integer, primary_key=True)
    EmpName = db.Column(db.String(200))
    Age = db.Column(db.Integer)

    departments = db.relationship('Department', secondary= empdpt)

    def __init__(self, empName, age):
        self.EmpName = empName
        self.Age = age


# creating department model
class Department(db.Model):
    __tablename__ = 'Department'
    Id = db.Column(db.Integer, primary_key=True)
    DepName = db.Column(db.String(200), unique=True)
    # employees = db.relationship('Employee', secondary= empdpt)

    def __init__(self, depName):
        self.DepName = depName

        


# returning the all departments
def retDept():
    return db.session.query(Department).all()

# returning the all departments
def retEmp():
    return db.session.query(Employee).all()

def retAssco():
    return db.session.query(empdpt).all()

# # return all employee details
# def retEmployeeList():
#     assoc = retAssco()

#     empDetails = list()

#     for i in assoc:
#         print(i)
#         emp = db.session.query(Employee).filter(Employee.Id == i[1])
#         depart =  db.session.query(Department).filter(Department.Id == i[2])
#         details = [emp, depart]
#         empDetails.append(details)

#     print(len(empDetails))

#     return empDetails

# rendering the first index page of website
@app.route('/')
def index():
    return render_template('index.html', data=retDept())

# on click add employee btn
@app.route('/addEmp', methods=['POST'])
def addEmp():
    if request.method == 'POST':
        empName = request.form['empName']
        empAge = request.form['empAge']
        empDept = request.form.get('empDept')

        print("\n\n", empName, empAge, empDept, "\n\n")
        print(empDept)

        if empName == '' or empAge == '' or empDept == '':
            return render_template('index.html', message='Please enter employee details...', classtype='warning', data=retDept())
        
        # dept = db.session.query(Department).filter(Department.DepName == empDept).first()
        # emp = db.session.query(Employee).filter(Employee.EmpName == empName and Employee.Age == empAge).first()

        # if emp is not None:
        #     result = db.session.execute('SELECT * FROM EmployeeDepartments WHERE empId = :val1 AND dptId = :val2' , {'val1': emp.Id, 'val2' : dept.Id}).count()
        #     if result == 0:
        #         return render_template('index.html', message='Department already allocated...', classtype='warning', data=retDept())
        # else:
        #     employee = Employee(empName, empAge)
        #     db.session.add(employee)
        #     db.session.commit()

        
        
        # return render_template('index.html', message='Employee details added successfully!', classtype='success', data=retDept())
        
        # return render_template('index.html', message='Department added successfully!', classtype='success', data=retDept())

        emp = None
        if db.session.query(Employee).filter(Employee.EmpName == empName and Employee.Age == empAge).count() == 0:
            emp = Employee(empName.upper(), empAge)
            db.session.add(emp)
            db.session.commit()

        dept = db.session.query(Department).filter(Department.DepName == empDept).first()

        # dept.employees.append(emp)

        # db.session.add(dept)
        try:
            emp.departments.append(dept)
            db.session.add(dept)
            db.session.commit()
        except:
            return render_template('index.html', message='Department already allocated...', classtype='warning', data=retDept())
        return render_template('index.html', message='Employee details added successfully!', classtype='success', data=retDept())



# on click add department btn
@app.route('/addDept', methods=['POST'])
def addDept():
    if request.method == 'POST':
        deptName = request.form['deptName']

        # print("\n\n", empDept, "\n\n")

        if deptName == '':
            return render_template('index.html', message='Please enter Department Name...', classtype='warning', data=retDept())

        if db.session.query(Department).filter(Department.DepName == deptName).count() == 0:
            data = Department(deptName)
            db.session.add(data)
            db.session.commit()
            return render_template('index.html', message='Department added successfully!', classtype='success', data=retDept())

        return render_template('index.html', message='Department already exits...', classtype='warning', data=retDept())


#  show emp list

# @app.route('/empList', methods=['GET'])
# def showEmpList():
#     if request.method == 'GET':
#         empList = retEmployeeList()
    
            
#         return render_template('EmployeeList.html', data=empList) 





if __name__ == "__main__":
    # for debugging 
    app.debug = True
    app.run()
