from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo



class CustomerForm(FlaskForm):
    SSN=StringField('Customer ID',validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    contact_no = StringField('Contact Number', validators=[DataRequired() ])
    gender = StringField('Gender', validators=[DataRequired()])
    dob=StringField('Date of Birth', validators=[DataRequired()])
    insurance_id= StringField('Insurance ID', validators=[ Length(max=10)])
    submit = SubmitField('Add / Update')


class LoginForm(FlaskForm) :
    #username = StringField('Student Name', validators=[DataRequired(), Length(min=2, max=50)])
    SSN=StringField('Employee ID',validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class EmployeeForm(FlaskForm):
    ID=StringField('Employee ID',validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    license= StringField('License')
    name = StringField('Name', validators=[DataRequired()])
    role= StringField('Role', validators=[DataRequired()])
    salary= IntegerField('Salary',validators=[DataRequired()])
    contact_no = StringField('Contact Number', validators=[DataRequired()])
    dob=StringField('Date of Birth', validators=[DataRequired()])
    submit = SubmitField('Update')



class InsuranceForm(FlaskForm):
    insurance_id=StringField('Insurance ID',validators=[DataRequired(),Length(min=5,max=5)])
    com_name = StringField('Company Name', validators=[DataRequired(), Length(max=20)])
    start_date=DateField('Start date', validators=[DataRequired()])
    end_date=DateField('Start date', validators=[DataRequired()])
    co_payment=IntegerField('Percentage of insurance cover', validators=[DataRequired()])
    submit=SubmitField('update')

class PrecriptionForm(FlaskForm):
    prescription_id=StringField('Prescription ID',validators=[DataRequired()])
    SSN=StringField('Customer ID',validators=[DataRequired()])
    doctor_name=StringField('Doctor name')
    prescription_date=StringField('Prescription date', validators=[DataRequired()])
    employee_id=StringField('Employee ID',validators=[DataRequired()])
    submit=SubmitField('Add')

class PrecribedDrugForm(FlaskForm):
    prescription_id=StringField('Prescription ID for Drug')
    drug_name1=StringField('Drug name')
    quantity1=IntegerField('Required quantity')
    drug_name2=StringField('Drug name')
    quantity2=IntegerField('Required quantity')
    drug_name3=StringField('Drug name')
    quantity3=IntegerField('Required quantity')
    drug_name4=StringField('Drug name')
    quantity4=IntegerField('Required quantity')
    drug_name5=StringField('Drug name')
    quantity5=IntegerField('Required quantity')
    submit= SubmitField('Add')


class MedicineForm(FlaskForm):
    drug_name=StringField('Drug Name',validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    manufacture = StringField('Name of manufacturer', validators=[DataRequired()])
    stock_quantity=IntegerField('Stock quantity', validators=[DataRequired()])
    expiry_date=StringField('Expiry date', validators=[DataRequired()])
    price=IntegerField('Price', validators=[DataRequired()])    
    submit= SubmitField('Add')

class BillForm(FlaskForm):
    prescription_id=StringField('Prescription ID for bill ',validators=[DataRequired()])
    submit=SubmitField('Generate Bill')


class BilldetailsForm(FlaskForm):
    bill_id=StringField('Bill ID', validators=[DataRequired(),Length(max=5)])
    prescription_id=StringField('Prescription ID',validators=[DataRequired(),Length(min=5,max=5)])
    SSN=StringField('Customer ID',validators=[DataRequired(),Length(min=5,max=5)])
    employee_id= StringField('Employee ID', validators=[DataRequired(), Length(max=5)])
    submit= SubmitField('Add')




