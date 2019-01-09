from flask import Flask ,session, render_template, request, redirect,url_for,g

from flask_mysqldb import MySQL

from flask_bcrypt import Bcrypt

import os
# intializing the app
app = Flask(__name__)
#secret key

app.secret_key= os.urandom(24)

# setting up database
app.config['MYSQL_HOST']='localhost'

app.config['MYSQL_USER']='root'

app.config['MYSQL_PASSWORD']= ''

app.config['MYSQL_DB']='crud'

mysql = MySQL(app)

#bcrypt for hashing passwords to keep database secure

bcrypt= Bcrypt(app)



@app.route('/',methods=['GET','POST'])
def index():

    if request.method=='GET':

        return render_template('login.html')

    else:

        form= request.form

        username=form['username']

        password=form['password']

        if username=='admin' and password=='admin':

            session['user']=username

            return redirect(url_for('data'))

        else:

            return redirect(url_for('index'))

@app.route('/list',methods=['GET'])

def data():

    if 'user' in session:

        cur = mysql.connection.cursor()

        resultValue = cur.execute(" select * from employee")

        userDetails = cur.fetchall()

        return render_template('list.html', employee=userDetails)

    else:

        return redirect(url_for('index'))



@app.route('/add',methods=['GET','POST'])

def add():
    if 'user' in session:

        if request.method == 'GET':

            return render_template('add.html')

        else:

            form = request.form

            print(form)

            firstname = form['firstname']

            lastname = form['lastname']

            address = form['address']

            email = form['email']

            contact = form['contact']

            argo = [firstname, lastname, address, email, int(contact)]

            cur = mysql.connection.cursor()

            cur.execute("INSERT INTO employee(firstname,lastname,address,email,contact) values (%s,%s,%s,%s,%s)", argo)

            mysql.connection.commit()

            cur.close()

            return redirect(url_for('data'))

    else:
        return redirect(url_for('index'))

@app.route('/delete/<id>',methods=['GET'])

def delete(id=None):
    if 'user' in session:

        query='delete from employee where id = %s'

        params=[id]

        cur = mysql.connection.cursor()

        cur.execute(query,params)

        mysql.connection.commit()

        cur.close()

        return redirect(url_for('data'))

    else:

        return redirect(url_for('index'))


@app.route('/edit/<id>',methods=['POST','GET'])

def edit(id=None):

    if 'user' in session:

        if request.method=='POST':

            form = request.form

            params=[form['firstname'],form['lastname'],form['address'],form['email'],form['contact'],id]

            query ='update employee set firstname= %s , lastname = %s , address= %s , email= %s, contact= %s where id = %s '

            cur = mysql.connection.cursor()

            cur.execute(query, params)

            mysql.connection.commit()

            cur.close()

            return redirect(url_for('data'))

        else:

            query = 'select * from employee where id = %s'

            params=[id]

            cur = mysql.connection.cursor()

            resultValue=cur.execute(query, params)

            if resultValue>0:

                userDetails = cur.fetchall()

                return render_template('edit.html',user=userDetails[0])

            else:

                return 'invalid id'
    else:

        return  redirect(url_for('index'))

@app.route('/logout',methods=['GET'])

def logout():

    session.pop('user', None)

    return redirect(url_for('index'))

if __name__=='__main__':

    app.run(debug=True)