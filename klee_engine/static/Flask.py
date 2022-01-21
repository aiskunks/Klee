from flask import Flask, render_template, request, session, g, redirect, url_for
import pyodbc
import re

app = Flask(__name__)
connection = pyodbc.connect('Driver=ODBC Driver 17 for SQL Server;'
                            'Server=DESKTOP-RJKRBE9;'
                            'Database=KLEE_USERS_DB;'
                            'UID=info7370;'
                            'PWD=info7370;'
                            'Trusted_Connection=yes;')

cursor = connection.cursor()
cursor.execute("CREATE TABLE [dbo].[KLEE_Users] (id INT IDENTITY(1,1) NOT NULL PRIMARY KEY, username  VARCHAR(80), email VARCHAR(200), password VARCHAR(100))")
connection.commit()


user = {"username": "abc", "password": "xyz"}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' or request.method == 'GET':
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def about():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        password = request.form['password']
        email = request.form['email']
        username = request.form['name']
        connection = pyodbc.connect('Driver=ODBC Driver 17 for SQL Server;'
                                    'Server=DESKTOP-RJKRBE9;'
                                    'Database=KLEE_USERS_DB;'
                                    'UID=info7370;'
                                    'PWD=info7370;'
                                    'Trusted_Connection=yes;')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM [dbo].[KLEE_Users] WHERE email = % s', (email,))
        account = cursor.fetchone()
        connection.commit()
        if account:
            msg = 'Account already exists !'
        else:
            cursor.execute('INSERT INTO [dbo].[KLEE_Users] VALUES (%s, % s, % s)', (username, email, password))
            connection.commit()
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/login_validation', methods=['POST','GET'])
def login_validation():
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        if username == user['username'] and password == user['password']:
            session['user'] = username
            return render_template('CSVtemplate.html')

        return "<h1>Wrong username or password</h1>"

    return render_template("login.html")

#      cur = mysql.connection.cursor()
   #     cur.execute("SELECT username,password FROM user WHERE username=%s", [uname])
   #     user = cur.fetchone()
   #     temp = user[1]

    #    if len(user) > 0:
     #       session.pop('username', None)
      #      if (bcrypt.check_password_hash(temp, passwrd)) == True:
       #         session['username'] = request.form['username']
        #        return render_template('home.html', uname=uname)
         #   else:
          #      flash('Invalid Username or Password !!')
           #     return render_template('login.html')
   # else:
    #    return render_template('login.html')

#@app.route("/Upload_Csv", methods=['POST'])

#def upload_csv():
   # target = os.path.join(APP_ROOT, 'C:/')
   # print(target)

   # if not os.path.isdir(target):
   #     os.mkdir(target)

  #  for file in request.files.getlist("file"):
   #     print(file)
  #      filename = file.filename


if (__name__ == "__main__"):
    app.run(port=5000)