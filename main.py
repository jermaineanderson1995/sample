from flask import Flask, render_template, flash, request, session, redirect, json
import os
import pymysql

db_user = os.environ.get('CLOUDSQL_USER')
db_password = os.environ.get('CLOUDSQL_PASSWORD')
db_name = os.environ.get('CLOUDSQL_DATABASE')
db_connection_name = os.environ.get('CLOUDSQL_CONNECTION_NAME')
db_connection_ip = os.environ.get('CLOUDSQL_IP')

app = Flask(__name__)
app.secret_key = b'\xb5\x18\x90d\xcd\xf7?\xab0\xd4[<)}\xb6\x1f\xbe\xd1r\xa0\xe2\x85S\xae'

# Route App Engine To Main Method
@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        # Save User Input
        input = request.form['input']
        if input != '':
            # Send User Input To Database Method
            return database(input)
        else:
            return render_template('index.html', respond='Can Not Leave Empty!')
    else:
        # Home Page Will Display On Start Up
        return list()


def database(input):
    try:
        # Connect To Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(host=db_connection_ip, user=db_user, password=db_password,
         db=db_name, charset='utf8', port=3306)
        # Create Cursor
        cursor = cnx.cursor()
        # Insert Data
        stm = "INSERT INTO info (name) VALUES (%s);"
        cursor.execute(stm, input)
        # Save Data
        cursor.execute('COMMIT;')
        cnx.close()
        # Display Success
        # return render_template('home.html', respond='Added To DB!')
        flash("Successfully added to DB.")
        return redirect('/')
        return render_template('index.html')
        # Connection Error
    except Exception:
        return render_template('index.html', respond='Could Not Connect To DB!')


def list():
    try:
        # Connect To Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(host=db_connection_ip, user=db_user, password=db_password,
         db=db_name, charset='utf8', port=3306)
        # Create Cursor
        cursor = cnx.cursor()
        cursor.execute('create table if not exists info (name varchar(255));')
        # Pull All Data From Database and Display
        cursor.execute('SELECT * FROM info;')
        result = cursor.fetchall()
        cnx.close()
        return render_template('index.html', names=result)
        # Connection Error
    except Exception:
        return render_template('index.html', respond='Could Not Connect To DB!')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
