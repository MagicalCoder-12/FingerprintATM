from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = 'welcome'
global uname

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['atm']
users_col = db['users']
transactions_col = db['transactions']

@app.route('/')
def home():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', msg='')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
   return render_template('Login.html', msg='')

@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    return render_template('Signup.html', msg='')

@app.route('/Deposit', methods=['GET', 'POST'])
def Deposit():
    output = '<tr><td><font size="3" color="black">Username</td><td><input type="text" name="t1" size="20" value='+uname+' readonly/></td></tr>'
    return render_template('Deposit.html', msg1=output)

@app.route('/Withdraw', methods=['GET', 'POST'])
def Withdraw():
    output = '<tr><td><font size="3" color="black">Username</td><td><input type="text" name="t1" size="20" value='+uname+' readonly/></td></tr>'
    return render_template('Withdraw.html', msg1=output)

@app.route('/Logout')
def Logout():
    return redirect('/index')

@app.route('/SignupAction', methods=['GET', 'POST'])
def SignupAction():
    if request.method == 'POST':
        user = request.form['t1']
        password = request.form['t2']
        phone = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        gender = request.form['t6']
        data = request.files['t7'].read()
        status = "none"

        if users_col.find_one({'username': user}):
            status = user + " Username already exists"
        else:
            users_col.insert_one({
                'username': user,
                'password': password,
                'contact_no': phone,
                'emailid': email,
                'address': address,
                'gender': gender
            })
            user_img_path = os.path.join('static', 'users', user + '.png')
            with open(user_img_path, "wb") as out_file:
                out_file.write(data)
            status = 'Signup process completed'
        return render_template('Signup.html', msg=status)

@app.route('/LoginAction', methods=['GET', 'POST'])
def LoginAction():
    global uname
    if request.method == 'POST':
        user = request.form['t1']
        password = request.form['t2']
        data = request.files['t3'].read()

        user_doc = users_col.find_one({'username': user, 'password': password})
        if user_doc:
            user_img_path = os.path.join('static', 'users', user + '.png')
            with open(user_img_path, "rb") as in_file:
                avail_data = in_file.read()
            if avail_data == data:
                uname = user
                return render_template('UserScreen.html', msg="Welcome " + uname)
        return render_template('Login.html', msg="Invalid login details")

def getAmount(user):
    last_txn = transactions_col.find_one(
        {'username': user}, sort=[('transaction_date', -1)]
    )
    return float(last_txn['total_balance']) if last_txn else 0

@app.route('/DepositAction', methods=['GET', 'POST'])
def DepositAction():
    if request.method == 'POST':
        user = request.form['t1']
        amount = float(request.form['t2'])
        total = getAmount(user) + amount
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        transactions_col.insert_one({
            'username': user,
            'transaction_amount': amount,
            'transaction_type': 'Deposit',
            'transaction_date': timestamp,
            'total_balance': total
        })
        return render_template('UserScreen.html', msg="Transaction Successful")

@app.route('/WithdrawAction', methods=['GET', 'POST'])
def WithdrawAction():
    if request.method == 'POST':
        user = request.form['t1']
        amount = float(request.form['t2'])
        total = getAmount(user)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if total >= amount:
            total -= amount
            transactions_col.insert_one({
                'username': user,
                'transaction_amount': amount,
                'transaction_type': 'Withdrawal',
                'transaction_date': timestamp,
                'total_balance': total
            })
            return render_template('UserScreen.html', msg="Withdrawal Transaction Successful")
        else:
            return render_template('UserScreen.html', msg="Insufficient Funds")

@app.route('/ViewBalance', methods=['GET', 'POST'])
def ViewBalance():
    font = "<font size='3' color='black'>" 
    output = ""
    rows = transactions_col.find({'username': uname})
    for row in rows:
        output += "<tr><td>"+font+str(row.get("username", ""))+"</td>"
        output += "<td>"+font+str(row.get("transaction_amount", ""))+"</td>"
        output += "<td>"+font+str(row.get("transaction_type", ""))+"</td>"
        output += "<td>"+font+str(row.get("transaction_date", ""))+"</td>"
        output += "<td>"+font+str(row.get("total_balance", ""))+"</td></tr>"
    return render_template('ViewBalance.html', msg=output)

if __name__ == '__main__':
    app.run(debug=True)
