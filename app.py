from flask import Flask, render_template, request, json, jsonify, redirect, url_for, session, send_file, make_response
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
import re
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import base64
import jwt
import datetime
from datetime import datetime
from datetime import timedelta



# import timedelta
matplotlib.use('Agg')

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

bcrypt = Bcrypt()

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'SAME_DB_Secret_key'
mysql = MySQL(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password123$'
app.config['MYSQL_DATABASE_DB'] = 'SAME_DB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# passenger_id_ct = int(100001)
# customer_id_ct = int(60001)

# @app.route("/")
# @cross_origin()
# def main():
#     return "Welcome!"

# conn = mysql.connect()
# cursor = conn.cursor()
# cursor.execute('call create_user(%s, %s, %s, %s);', (59, 'aman4', 'jaljfjafjafkljabfa', 'abc@xyz.com',))
# conn.commit()
# print(cursor.fetchone())


@app.route('/test')
def test():
    # hash = bcrypt.generate_password_hash('cairocoders')
    # check_hash = bcrypt.check_password_hash(hash, 'cairocoders')
    # for passenger in session['Passengers']:
    #     print(passenger)
    #     if passenger['passenger_type'] == 'C':
    #         # print(passenger)
    #         passengerid = passenger['passengerid']
    if not session['Passengers']:
        session['Passengers'] = []
        print("no passenger")
    print('test run')
    return "test"
    # return render_template('index.html', session = session)

@app.route('/')
def index():
    # hash = bcrypt.generate_password_hash('cairocoders')
    # check_hash = bcrypt.check_password_hash(hash, 'cairocoders')
    return render_template('index.html', session = session)

@app.route('/home')
def home():
    return render_template('index.html', session = session)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    print('here')
    if request.method == 'GET':
        return render_template('login_flask.html')
    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    # if request.json['username'] and request.json['password']:
    # if True:
    if request.form['username'] and request.form['password']:
        print('here2')
        # for react
        # print(request.json['username'])
        # username = "aman"
        # username = request.json['username']
        username = request.form['username']
        password = request.form['password']
        # password = request.json['password']
        # for postman
        # username = request.args.get('username')
        # password = request.args.get('password')
        print('username', username, 'pass', password)
        conn = mysql.connect()
        cursor = conn.cursor()
        # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # print(hashed_password)
        # We will have to take password corresponding to an username, then check that with the input password.
        # bcrypt.check_password_hash(hashed_password, password)
        cursor.execute('call login(%s);', (username,))
        account = cursor.fetchone()


        print(account)
        if account:
            print('account exists')
            if bcrypt.check_password_hash(account[2], password):
                print('Here with password: ', account[2])
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                token = jwt.encode({
                    'public_id': username,
                    'exp': datetime.utcnow() + timedelta(minutes=30)
                }, app.config['SECRET_KEY'])
                print(token)
                return make_response(jsonify({'token': token}), 201)
                # return 'Logged in successfully! with email: ' + account[3]
            else:
                msg = 'Incorrect username/password!'
                return 'No-data'
        return msg
    # return render_template('index.html', msg=msg)


@app.route('/logout/')
def logout():
    print('logging out')
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    print('logged out')
    # return "Succesfully Logged Out TEST"
    for key in list(session.keys()):
        session.pop(key, None)
    print('session', session)
    session.clear()
    # return render_template('index.html', session = session)
    return redirect(url_for('home'))


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'GET':
        return render_template('signup.html')
    if True:
    # if request.method == 'POST' and request.args.get('username') and request.args.get('password') and request.args.get('c_email'):
    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        print("here")
        #     Keep this id same as the customer id
        # id = request.args.get('id')
        username = request.form['username']
        password = request.form['password']
        print(username)
        # passengerid = request.args.get('passengerid')
        # customerid = request.args.get('customerid')

        # customer_type = request.args.get('customer_type')
        # c_street = request.args.get('c_street')
        # c_city = request.args.get('c_city')
        # c_state = request.args.get('c_state')
        # c_zipcode = request.args.get('c_zipcode')
        c_email = request.form['email']
        # print(c_email)
        print(username, password, c_email)
        # print(password)
        # c_contactnumber = request.args.get('c_contactnumber')
        # c_contact_countrycode = request.args.get('c_contact_countrycode')
        # number_of_passengers = request.args.get('number_of_passengers')
        # em_fname = request.args.get('em_fname')
        # em_lname = request.args.get('em_lname')
        # em_contactnumber = request.args.get('em_contactnumber')
        # em_contact_countrycode = request.args.get('em_contact_countrycode')

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', c_email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not c_email:
            msg = 'Please fill out the form!'
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            print(hashed_password)
            # global customer_id_ct
            # global passenger_id_ct
            # temp_id = int(73)

            cursor.execute('select * from asst_customer order by customerid desc LIMIT 1')
            customerid = cursor.fetchone()
            customerid = int(customerid[1])
            customerid = customerid + 1

            cursor.execute('call create_user(%s, %s, %s, %s);', (customerid, username, hashed_password, c_email,))

            conn.commit()
            msg = 'You have successfully registered!'
            print(msg)
    else:
        msg = 'Please fill out the form!'
    print(msg)
    # return render_template('Display.html', msg=msg)
    # return redirect(url_for('login'))
    return jsonify({'url': '/home'})


# dept_apt:dept_apt, arv_apt:arv_apt, dept_date: dept_date, arv_date:arv_date, no_of_passengers: no_of_passengers
@app.route('/add_booking_details', methods=['GET', 'POST'])
def add_booking_details():
    if session['loggedin'] == False:
        return render_template('login_flask.html')
    elif request.method == 'GET' and session['loggedin'] == True:
        return render_template('booking_final.html')
    else:
        # print(request.form)
        dept_apt = request.form['dept_apt']
        arv_apt = request.form['arv_apt']
        dept_date = request.form['dept_date']
        arv_date = request.form['arv_date']
        no_of_passengers = request.form['no_of_passengers']


        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('select * from asst_airport where airport_name= %s', (dept_apt,))
        account = cursor.fetchone()
        dept_apt_code = account[0]

        cursor.execute('select * from asst_airport where airport_name= %s', (arv_apt,))
        account = cursor.fetchone()
        arv_apt_code = account[0]

        # session['dept_apt_code'] = dept_apt_code
        # session['arv_apt_code'] = arv_apt_code
        # session['dept_date'] = dept_date
        # session['arv_date'] = arv_date
        # session['no_of_passengers'] = no_of_passengers

        cursor.execute('select * from asst_flight order by flightid desc LIMIT 1')
        flightid = cursor.fetchone()
        flightid = int(flightid[0])
        flightid = flightid + 1
        print(flightid)

        # session['flightid'] = flightid

        Booking_Details = {
            'dept_apt_code': dept_apt_code,
            'arv_apt_code': arv_apt_code,
            'dept_date': dept_date,
            'arv_date': arv_date,
            'no_of_passengers': no_of_passengers,
            'flighid': flightid
        }

        # cursor.execute('insert into asst_flight values(%s, %s, %s, %s, %s)', (flightid, dept_date,
        #                                                                 arv_date, dept_apt_code, arv_apt_code))

        # conn.commit();


        session['Booking_Details'] = Booking_Details
        print(session)
        print('end')
        print(session['Booking_Details'])

        return render_template('passenger_final.html')
        # return redirect(url_for('passenger_details'))
        # return jsonify(Booking_Details)


@app.route('/passenger_details', methods=['GET', 'POST'])
def passenger_details():
    if session['loggedin'] == False:
        return render_template('login_flask.html')
    elif request.method == 'GET' and session['loggedin'] == True:
        return render_template('passenger_final.html')
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        nationality = request.form['nationality']
        dob = request.form['dob']
        passport_no = request.form['passport_no']
        expiry_date = request.form['expiry_date']
        cabin_class = request.form['cabin_class']
        meal_plan = request.form['meal_plan']
        special_request = request.form['special_request']
        passenger_type = request.form['passenger_type']
        add_pass = request.form['add_pass']

        conn = mysql.connect()
        cursor = conn.cursor()

        print(meal_plan)
        cursor.execute('select * from asst_meal_plan where mealplan_name = %s', (meal_plan,))
        meal_plan_code = cursor.fetchone()
        meal_plan_code = meal_plan_code[0]

        print(cabin_class)
        cursor.execute('select * from asst_cabin_class where cabin_class_type = %s', (cabin_class,))
        cabin_class_id = cursor.fetchone()
        cabin_class_id = cabin_class_id[0]

        print(special_request)
        cursor.execute('select * from asst_special_assistance where spl_asst_name = %s', (special_request,))
        splasstid = cursor.fetchone()
        splasstid = splasstid[0]


        cursor.execute('select * from asst_passenger order by passengerid desc LIMIT 1')
        passengerid = cursor.fetchone()
        passengerid = int(passengerid[0])
        passengerid = passengerid + 1
        if 'Passengers' not in session:
            session['Passengers'] = []

        Passenger = {
            'passengerid': passengerid,
            'passenger_type': passenger_type,
            'fname': fname,
            'lname': lname,
            'gender': gender,
            'nationality': nationality,
            'dob': dob,
            'passport_no': passport_no,
            'expiry_date': expiry_date,
            'cabin_class': cabin_class_id,
            'meal_plan': meal_plan_code,
            'special_request': splasstid,
        }
        session['Passengers'].append(Passenger)
        print(session)

        if add_pass == 'True':
            return jsonify({'url':'/passenger_details'})
            # return redirect(url_for('passenger_details'))


        cursor.execute('select * from accounts where username = %s', (session['username']))
        id = cursor.fetchone()
        id = id[0]
        cursor.execute('select * from asst_customer where customerid=%s', (id,))
        cust_already = cursor.fetchone()
        # When inserting the data check if customer_already = True, loop through the passenger ids
        # to get the updated passengerid of the customer, and also fetch the customer id using logged in user.
        if cust_already:
            session['Customer_Already'] = True
            return jsonify({'url': '/insurance'})

        return jsonify({'url': '/customer_details'})
            # return render_template('insurance.html')
        # return render_template('customer.html')
        # return jsonify(Passenger)


@app.route('/customer_details', methods=['GET', 'POST'])
def customer_details():
    if session['loggedin'] == False:
        return render_template('login_flask.html')
    elif request.method == 'GET' and session['loggedin'] == True:
        return render_template('customer.html')
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        em_fname = request.form['em_fname']
        em_lname = request.form['em_lname']
        customer_type = request.form['customer_type']
        street = request.form['street']
        city = request.form['city']
        zipcode = request.form['zipcode']
        email = request.form['email']
        c_country_code = request.form['c_country_code']
        # insurances = request.form['insurances']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('select * from asst_customer order by customerid desc LIMIT 1')
        customerid = cursor.fetchone()
        customerid = int(customerid[0])
        customerid = customerid + 1

        for passenger in session['Passengers']:
            if passenger['passenger_type'] == 'C':
                passengerid = passenger['passengerid']

        Customer_Details = {
            'passengerid': passengerid,
            'customerid': customerid,
            'customer_type': customer_type,
            'fname': fname,
            'lname': lname,
            'em_fname': em_fname,
            'em_lname': em_lname,
            'street': street,
            'city': city,
            'zipcode': zipcode,
            'email': email,
            'c_country_code': c_country_code,
        }

        session['Customer_Details'] = Customer_Details
        return jsonify({'url': '/insurance_selection'})


@app.route('/insurance_selection', methods=['GET', 'POST'])
def insurance_selection():
    print('Here in insurance')
    # print(request.form['insurances'])
    # print(request.form)
    if session['loggedin'] == False:
        return render_template('login_flask.html')
    elif request.method == 'GET' and session['loggedin'] == True:
        return render_template('insurance.html')
    else:
        # insurances = request.json['insurances']
        # session['insurances'] = insurances
        # print(request.form)
        conn = mysql.connect()
        cursor = conn.cursor()
        insurance_details = []

        # for insurance_plan in request.form.getlist('insurances'):
        #     print(insurance_plan)

        insurances = request.form.getlist('insurances')
        total = 0
        for insurance_plan in insurances:
            # print('Ins plan: ',insurance_plan)
            cursor.execute("select * from asst_insurance_plans where plan_name =%s", (insurance_plan,))
            row = cursor.fetchone()
            plan_name = row[1]
            unit_price = row[2]
            no_of_passengers = session['Booking_Details']['no_of_passengers']
            total = total + int(unit_price) * int(no_of_passengers)
            insurance_details.append({
                'plan_name': plan_name,
                'unit_price': int(unit_price),
                'no_of_passengers': int(no_of_passengers)
            })
        print(total)
        cursor.execute('select * from asst_invoice order by invoice_number desc Limit 1')
        invoice_no = cursor.fetchone()
        invoice_no = int(invoice_no[0])
        invoice_no = invoice_no + 1

        invoice_date = datetime.today().strftime('%Y-%m-%d')

        session['invoice_no'] = invoice_no
        session['invoice_date'] = invoice_date
        session['insurance_details'] = insurance_details
        session['total'] = total
        session['tax'] = total/10

        print('success')
        return jsonify({'Message': 'Insurance Selected Successfully.'})

# Payment_Method:payment_method, Card_Number:card_number,fname:fname, lname:lname, expiry_date:expiry_date
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    print('Here in Payment')
    if session['loggedin'] == False:
        return render_template('login_flask.html')
    elif request.method == 'GET' and session['loggedin'] == True:
        return render_template('payment.html')
    else:
        payment_method = request.form['payment_method']
        card_number = request.form['card_number']
        fname = request.form['fname']
        lname = request.form['lname']
        expiry_date = request.form['expiry_date']
        payment_date = datetime.today().strftime('%Y-%m-%d')

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('select * from asst_payment order by paymentid desc Limit 1')
        paymentid = cursor.fetchone()
        paymentid = int(paymentid[0])
        paymentid = paymentid + 1

        session['paymentid'] = paymentid
        session['payment_method'] = payment_method
        session['card_number'] = card_number
        session['fname'] = fname
        session['lname'] = lname
        session['expiry_date'] = expiry_date
        session['payment_date'] = payment_date

        print('Payment Details Stored')
        return jsonify({'url': '/generate_invoice'})


@app.route('/generate_invoice', methods=['GET', 'POST'])
def generate_invoice():
    print('Here in invoice')
    # print(request.form['insurances'])
    # print(request.form)
    if session['loggedin'] == False:
        return render_template('login_flask.html')
    elif request.method == 'GET' and session['loggedin'] == True:
        return render_template('invoice.html', invoice_no=session['invoice_no'], username=session['username'],
                               invoice_date=session['invoice_date'], insurance_details=session['insurance_details'],
                               total=int(session['total']), tax=int(session['tax']))



@app.route('/visualizations', methods=['GET', 'POST'])
def visualizations():
    if session['loggedin'] == False:
        return render_template('login_flask.html')
    elif request.method == 'GET' and session['loggedin'] == True:
        conn = mysql.connect()
        cursor = conn.cursor()
        # cursor.execute("Select * from authors;")
        cursor.execute("select a.planid, b.plan_name from asst_insrplans_customer a, asst_insurance_plans b where a.planid = b.planid;")
        df = pd.DataFrame(cursor, columns=['planid', 'plan_name'])
        data = df['plan_name'].value_counts().sort_values(ascending=False)[:3]
        points = data.index
        frequency = data.values
        plt.bar(points, frequency)
        plt.title('Top 3 Most Purchased Insurance Plans')

        plt.xlabel('Plan Name')
        plt.ylabel('Number of Times Purchased')
        base_addr = '/Users/saimbhi/PycharmProjects/DBMS_Project/templates/static/images/Top4.png'
        plt.savefig(base_addr)
        with open(base_addr, mode='rb') as file:
            image = file.read()
        img = base64.encodebytes(image).decode("utf-8")
        # return render_template('visualization.html', img=img)
        # return jsonify({'Visualization': img})
        # return "all good"
        return send_file(base_addr, mimetype='image/gif')


if __name__ == "__main__":
    app.run()




# $2b$12$ez4vQx6Rcbmnj9CL4FIkqO2yjDkJmLmFToPjI/DOTpyq1oRD/dup2
# user = test
# password = password