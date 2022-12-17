from flask import Flask, render_template, flash, redirect, request, session,redirect,url_for
from flask_mysqldb import MySQLdb
from flask_mysqldb import MySQL
from forms import *
import MySQLdb.cursors


import re
import hashlib
import string

app=Flask(__name__)
# app.secret_key="manaskulkarni"


app.config['SECRET_KEY'] = '4e9c884a5a717a5980682d23c6cbf27c'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'phmk'

mysql=MySQL(app)

@app.route('/', methods=['GET','POST'])
def login():
    try:
        if session['loggedin']:
            flash(
                f"You are already logged in as {session['username']}", 'danger')
            return redirect('home')
    except:
        pass
    form = LoginForm()
    msg = ''
    if request.method == 'POST' and form.SSN.data and form.password.data:
        SSN = form.SSN.data
        password = form.password.data
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM employee WHERE ID = % s AND password = % s', (SSN, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[0]
            msg = 'Logged in successfully !'
            redirect('home')
            flash(msg, 'success')
        else:
            msg = 'Incorrect username / password !'
            flash(msg, 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        if session['loggedin']:
            pass

    except:
        info_list = [
            {
                'SSN': '',
                'password': ''
            }
        ]
        flash("Log in to see your profile page", 'warning')
        redirect('/') 
        

    SSN = session['username']

    if SSN == '99999':
        info_list = [{
            'SSN': '99999',
            'password': 'admin@123'
        }]
        return render_template('index.html', title='Home')

    return render_template('index.html', title='Home')
      


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    try:
        if session['loggedin']:
            session.pop('loggedin', None)
            session.pop('id', None)
            session.pop('username', None)
    except:
        flash("You are not logged in", 'danger')
    return redirect('/')


@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in as admin", 'warning')
        return redirect('/')

    if session['username'] != "99999":
        flash("You are not logged in as admin", 'warning')
        return redirect('/')
    
    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        ID=form.ID.data
        cursor.execute(
                'SELECT * FROM employee WHERE ID = %s', [ID])
        a = cursor.fetchone()
        print("0")
        if not a:
            cursor.execute('INSERT INTO employee VALUES(% s, % s, %s, %s, %s, %s, %s, %s)', (
                ID, form.password.data,form.license.data, form.name.data, form.role.data,form.salary.data, form.contact_no.data, form.dob.data))
            mysql.connection.commit()
            print("1")
        else:
            cursor.execute('UPDATE employee SET password = %s, license = %s, name = %s, role = %s, salary = %s, phone_no = %s, dob = %s where ID = %s',
                            (form.password.data,form.license.data, form.name.data, form.role.data,form.salary.data, form.contact_no.data, form.dob.data, ID))
            #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())
            print("2")
            mysql.connection.commit()
        flash("Employee Added", 'warning')
        return redirect('home')
    else:
        flash("Please enter your details in correct format.", 'danger')
    return render_template('add-employee.html', title='Add-Employee', form=form)



@app.route('/show-employee', methods=['GET', 'POST'])
def show_employee():
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in as admin", 'warning')
        return redirect('home')

    if session['username'] != "99999":
        flash("You are not logged in as admin", 'warning')
        return redirect('home')
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT * FROM employee ')
    table = cursor.fetchall()
    # cursor.execute(
    #     'SELECT MIS, transaction_id, payment_date FROM (stays_in NATURAL JOIN (pays NATURAL JOIN Fees))')
    # table1 = cursor.fetchall()
    return render_template('show-employee.html', table=table)



@app.route('/customer', methods=['GET', 'POST'])
def show_customer():
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in as admin", 'warning')
        return redirect('home')

    # if session['username'] != "99999":
    #     flash("You are not logged in as admin", 'warning')
    #     return redirect('home')
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT * FROM customer ')
    table = cursor.fetchall()
    # cursor.execute(
    #     'SELECT MIS, transaction_id, payment_date FROM (stays_in NATURAL JOIN (pays NATURAL JOIN Fees))')
    # table1 = cursor.fetchall()
    return render_template('customer.html', table=table)

@app.route('/add-customer', methods=['GET', 'POST'])
def add_customer():
    form = CustomerForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in", 'warning')
        return redirect('/')
    
    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        SSN=form.SSN.data
        cursor.execute(
                'SELECT * FROM customer WHERE SSN = %s', [SSN])
        a = cursor.fetchone()
        print("0")
        if not a:
            cursor.execute('INSERT INTO customer VALUES(%s, %s, %s, %s, %s)', (
                SSN, form.name.data,form.contact_no.data, form.gender.data, form.dob.data))
            mysql.connection.commit()
            print("1")
        else:
            cursor.execute('UPDATE customer SET name = %s, phone = %s, gender = %s, dob = %s where SSN = %s',
                            (form.name.data,form.contact_no.data, form.gender.data, form.dob.data, SSN))
            #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())
            print("2")
            mysql.connection.commit()
        flash("Customer Added", 'warning')
        return redirect('customer')
    else:
        flash("Please enter your details in correct format.", 'danger')
    return render_template('add-customer.html', title='Add-Customer', form=form)



@app.route('/show-medicine', methods=['GET', 'POST'])
def medicines():
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in as admin", 'warning')
        return redirect('home')

    if session['username'] != "99999":
        flash("You are not logged in as admin", 'warning')
        return redirect('home')
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT * FROM medicine ')
    table = cursor.fetchall()
    # cursor.execute(
    #     'SELECT MIS, transaction_id, payment_date FROM (stays_in NATURAL JOIN (pays NATURAL JOIN Fees))')
    # table1 = cursor.fetchall()
    return render_template('medicine.html', table=table)



@app.route('/add-medicine', methods=['GET', 'POST'])
def add_medicine():
    form = MedicineForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in as admin", 'warning')
        return redirect('/')

    if session['username'] != "99999":
        flash("You are not logged in as admin", 'warning')
        return redirect('/')
    
    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        drug_name=form.drug_name.data
        cursor.execute(
                'SELECT * FROM medicine WHERE drug_name = %s', [drug_name])
        a = cursor.fetchone()
        print("0")
        if not a:
            cursor.execute('INSERT INTO medicine VALUES(% s, % s, %s, %s, %s, %s)', (
                drug_name, form.type.data,form.manufacture.data, form.stock_quantity.data, form.expiry_date.data,form.price.data))
            mysql.connection.commit()
            print("1")
        else:
            cursor.execute('UPDATE medicine SET type = %s, manuf = %s, stock_qt = %s, exp_date = %s, price = %s where drug_name = %s',
                            (form.type.data,form.manufacture.data, form.stock_quantity.data, form.expiry_date.data,form.price.data,drug_name))
            #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())
            print("2")
            mysql.connection.commit()
        flash("Medicine Added", 'warning')
        return redirect('show-medicine')
    else:
        flash("Please enter your details in correct format.", 'danger')
    return render_template('add-medicine.html', title='Add-Medicine', form=form)



@app.route('/prescription', methods=['GET', 'POST'])
def show_prescription():
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in ", 'warning')
        return redirect('/')

    # if session['username'] != "99999":
    #     flash("You are not logged in as admin", 'warning')
    #     return redirect('home')
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT * FROM prescription ')
    table = cursor.fetchall()
    # cursor.execute(
    #     'SELECT MIS, transaction_id, payment_date FROM (stays_in NATURAL JOIN (pays NATURAL JOIN Fees))')
    # table1 = cursor.fetchall()
    return render_template('prescription.html', table=table)


f=0
@app.route('/add-prescription', methods=['GET', 'POST'])
def add_prescription():
    form = PrecriptionForm()
    form1 = PrecribedDrugForm() 
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in", 'warning')
        return redirect('/')
    global f
    if f==0:
        if request.method == 'POST' and form.validate_on_submit():
            cursor = mysql.connection.cursor()
            prescription_id=form.prescription_id.data
            cursor.execute(
                    'SELECT * FROM prescription WHERE prescription_id = %s', [prescription_id])
            a = cursor.fetchone()
            print("0")
            if not a:
                cursor.execute('INSERT INTO prescription VALUES(%s, %s, %s, %s, %s)', (
                    prescription_id, form.SSN.data,form.doctor_name.data, form.prescription_date.data, form.employee_id.data))
                mysql.connection.commit()
                print("1")
            else:
                cursor.execute('UPDATE customer SET SSN = %s, doc_name = %s, pres_date = %s, ID = %s where prescription_id = %s',
                                (form.SSN.data,form.doctor_name.data, form.prescription_date.data, form.employee_id.data ,prescription_id))
                #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())
                print("2")
                mysql.connection.commit()
            flash("Prescription  Added", 'warning')
            f=1
            return render_template('add-prescription-drug.html', title='Add-Prescription-DRUG', form=form1)
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        prescription_id=form1.prescription_id.data
        if(form1.drug_name1.data):
            cursor.execute('INSERT INTO prescribed_drug VALUES(%s, %s, %s)', (
                prescription_id, form1.drug_name1.data,form1.quantity1.data))
            mysql.connection.commit()
        if(form1.drug_name2.data):
            cursor.execute('INSERT INTO prescribed_drug VALUES(%s, %s, %s)', (
                prescription_id, form1.drug_name2.data,form1.quantity2.data))
            mysql.connection.commit()
        if(form1.drug_name3.data):
            cursor.execute('INSERT INTO prescribed_drug VALUES(%s, %s, %s)', (
                prescription_id, form1.drug_name3.data,form1.quantity3.data))
            mysql.connection.commit()
        if(form1.drug_name4.data):
            cursor.execute('INSERT INTO prescribed_drug VALUES(%s, %s, %s)', (
                prescription_id, form1.drug_name4.data,form1.quantity4.data))
            mysql.connection.commit()
        if(form1.drug_name5.data):
            cursor.execute('INSERT INTO prescribed_drug VALUES(%s, %s, %s)', (
                prescription_id, form1.drug_name5.data,form1.quantity5.data))
            mysql.connection.commit()
        return redirect('/home')
    return render_template('add-customer.html', title='Add-Customer', form=form)




@app.route('/add-prescribed-drug', methods=['GET', 'POST'])
def add_prescribed_drug():
    form = PrecribedDrugForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in", 'warning')
        return redirect('/')
    
    if request.method == 'POST' and form.validate_on_submit():
        prescription_id = form.prescription_id.data
        cursor = mysql.connection.cursor()
        prescription_id=form.prescription_id.data
        cursor.execute(
                'SELECT * FROM prescription WHERE prescription_id = %s', [prescription_id])
        a = cursor.fetchone()
        print("0")
        if not a:
            cursor.execute('INSERT INTO prescription VALUES(%s, %s, %s, %s, %s)', (
                prescription_id, form.SSN.data,form.doctor_name.data, form.prescription_date.data, form.employee_id.data))
            mysql.connection.commit()
            print("1")
        else:
            cursor.execute('UPDATE customer SET SSN = %s, doc_name = %s, pres_date = %s, ID = %s where prescription_id = %s',
                            (form.SSN.data,form.doctor_name.data, form.prescription_date.data, form.employee_id.data ,prescription_id))
            #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())
            print("2")
            mysql.connection.commit()
        flash("Prescription  Added", 'warning')
        return redirect('prescription')
    else:
        flash("Please enter your details in correct format.", 'danger')
    return render_template('add-prescription-drug.html', title='Add-Customer', form=form)





@app.route('/bill-generate', methods=['GET', 'POST'])
def bill_generate():
    form = BillForm()
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in", 'warning')
        return redirect('/')
    
    if request.method == 'POST' and form.validate_on_submit():
        cursor = mysql.connection.cursor()
        prescription_id=form.prescription_id.data
        cursor.execute(
                'SELECT SUM(price) FROM medicine WHERE drug_name IN (SELECT drug_name FROM prescribed_drug WHERE prescription_id=%s )', [prescription_id])
        a = cursor.fetchone()
        cursor.execute('INSERT INTO bill VALUES(%s, %s, %s, %s, %s)', (
            prescription_id, prescription_id,a, a, 0))
        mysql.connection.commit()
          
        # print("0")
        # if not a:
        #     cursor.execute('INSERT INTO customer VALUES(%s, %s, %s, %s, %s)', (
        #         SSN, form.name.data,form.contact_no.data, form.gender.data, form.dob.data))
        #     mysql.connection.commit()
        #     print("1")
        # else:
        #     cursor.execute('UPDATE customer SET name = %s, phone = %s, gender = %s, dob = %s where SSN = %s',
        #                     (form.name.data,form.contact_no.data, form.gender.data, form.dob.data, SSN))
        #     #cursor.execute('INSERT INTO Student_Info VALUES (% s, % s, %s, %s, %s, %s, %s, %s)', ())
        #     print("2")
        #     mysql.connection.commit()
        flash("Bill generated", 'warning')
        return redirect('bills')
    else:
        flash("Please enter your details in correct format.", 'danger')
    return render_template('add-bill.html', title='Add-bill', form=form)


@app.route('/bills', methods=['GET', 'POST'])
def show_bill():
    try:
        if session['loggedin']:
            pass
    except:
        flash("You are not logged in ", 'warning')
        return redirect('/')

    # if session['username'] != "99999":
    #     flash("You are not logged in as admin", 'warning')
    #     return redirect('home')
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT * FROM bill ')
    table = cursor.fetchall()
    # cursor.execute(
    #     'SELECT MIS, transaction_id, payment_date FROM (stays_in NATURAL JOIN (pays NATURAL JOIN Fees))')
    # table1 = cursor.fetchall()
    return render_template('prescription.html', table=table)






if __name__ == '__main__':
    app.run(debug=True)
