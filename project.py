import pymysql
from app import app
from flask_mysqldb import MySQL
from db import mysql
from flask import jsonify
from flask import flash, request  


@app.route('/addEmployee', methods = ['GET', 'POST'])
def add_employee():
    _json = request.json
    _first_name = _json['first_name']
    _last_name = _json['last_name']
    _email = _json['email']
    _birth_day = _json['birth_day']
    _sex = _json['sex']
    _dept_id = _json['dept_id']
    _comp_id = _json['comp_id']

    if request.method == "POST":
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO employee(first_name, last_name, email, birth_day, sex, dept_id, comp_id) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        data = (_first_name, _last_name, _email, _birth_day, _sex, _dept_id, _comp_id)
        cursor.execute(sql,data)
        mysql.connection.commit()
        resp = jsonify("User added successfully!")
        resp.status_code = 200
        return resp
    else: 
        return not_found()
        
@app.route('/updatecompany/<emp_id>', methods = ['GET','POST'])
def update_company(emp_id):
    try:
        _json = request.json
        _emp_id = _json['emp_id']
        _comp_id = _json['comp_id']
        cursor = mysql.connection.cursor()
        sql = "SELECT* FROM employee where emp_id = %s"
        result = cursor.execute(sql,(_emp_id))
        if result == 0:
            resp = jsonify("There is no such employee")
        else:
            sql = "UPDATE employee SET comp_id = %s WHERE emp_id = %s"
            data = (_comp_id,_emp_id)
            cursor.execute(sql,data)
            mysql.connection.commit()
            resp = jsonify("Company updated successfully!")
            resp.status_code = 200
            return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()

    

@app.route('/deleteemployee/<emp_id>', methods = ['GET','POST'])
def delete_employee(emp_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM employee WHERE emp_id = %s",(emp_id,))
        mysql.connection.commit()
        resp = jsonify("User deleted successfully!")
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()

@app.route('/department', methods = ['GET'])
def list_department():
    cursor = mysql.connection.cursor()
    sql = "SELECT* From department"
    cursor.execute(sql)
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    return resp

@app.route('/company', methods = ['GET'])
def list_company():
    cursor = mysql.connection.cursor()
    sql = "SELECT DISTINCT comp_name, first_name, last_name FROM employee, company WHERE employee.comp_id = company.comp_id"
    cursor.execute(sql)
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    return resp

@app.route('/deptOfemployee', methods = ['GET'])
def dept_employee():
    cursor = mysql.connection.cursor()
    sql = "SELECT DISTINCT comp_name, dept_name, first_name, last_name FROM employee, department, company WHERE employee.comp_id = company.comp_id and employee.dept_id = department.dept_id"
    cursor.execute(sql)
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    return resp


if __name__ == "__main__":
    app.run(debug = True)
