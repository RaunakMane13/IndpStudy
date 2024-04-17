from markupsafe import escape
from flask import Flask, request, render_template_string, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import mysql.connector
import csv
import os
app = Flask(__name__)
app.secret_key = 'your_very_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

@app.route('/', methods=['GET', 'POST'])
def root_login():
    if request.method == 'POST':
        root_username = request.form['username']
        root_password = request.form['password']
        try:
            # Attempt to establish a connection using root credentials
            connection = mysql.connector.connect(host='localhost', user=root_username, password=root_password)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SHOW DATABASES")
                databases = [db[0] for db in cursor.fetchall()]
                cursor.close()
                connection.close()
                session['root_credentials'] = {'username': root_username, 'password': root_password}
                session['databases'] = databases
                return redirect(url_for('select_database'))
        except mysql.connector.Error as err:
            # Detailed error message might help diagnose the issue
            return f"Root login failed: {str(err)}"
    return render_template_string("""
        <style>
            input[type=text], input[type=password], input[type=submit] {
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            input[type=submit] {
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
            }
            input[type=submit]:hover {
                background-color: #45a049;
            }
        </style>
        <form method="post">
            Root Username: <input type="text" name="username"><br>
            Root Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    """)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/select_database', methods=['GET', 'POST'])
def select_database():
    if 'databases' not in session:
        return redirect(url_for('root_login'))
    
    # Handle selection of existing database and direct redirection to phpMyAdmin
    if request.method == 'POST' and 'database' in request.form:
        selected_database = request.form['database']
        if selected_database in session['databases']:
            session['selected_database'] = selected_database
            # Construct the phpMyAdmin URL and redirect
            phpmyadmin_url = f"http://localhost/phpmyadmin/index.php?db={session['selected_database']}"
            return redirect(phpmyadmin_url)
    
    databases_html = '<form method="post">'
    for db in session['databases']:
        databases_html += f'<button type="submit" name="database" value="{escape(db)}">{escape(db)}</button><br>'
    databases_html += '</form>'
    
    # Append the form for new database creation and CSV upload to databases_html
    databases_html += '''
        <hr>
        <form method="post" enctype="multipart/form-data">
            New Database Name: <input type="text" name="new_database" required><br>
            CSV File: <input type="file" name="file" accept=".csv" required><br>
            <input type="submit" value="Create Database and Upload CSV">
        </form>
    '''
    
    return render_template_string('''
        {{ databases_html|safe }}
        <style>
            input, button[type=submit] {
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            button[type=submit], input[type=submit] {
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
                border: none;
  }
            button[type=submit]:hover, input[type=submit]:hover {
                background-color: #45a049;
            }
            form {
                margin-top: 20px;
            }
        </style>
    ''', databases_html=databases_html)



def create_database_and_table_from_csv(root_credentials, database_name, file_path):
    connection = mysql.connector.connect(**root_credentials)
    cursor = connection.cursor()
    
    # Create database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
    connection.commit()
    
    cursor.execute(f"USE `{database_name}`")
    
    # Read CSV file and prepare for table creation and data insertion
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Assuming the first row is headers
        
        # Determine data types from the first row of data
        first_row = next(reader, None)
        data_types = ['FLOAT' if value.replace('.', '', 1).isdigit() else 'INT' if value.isdigit() else 'VARCHAR(255)' for value in first_row]
        
        # Construct CREATE TABLE statement
        table_name = os.path.splitext(os.path.basename(file_path))[0].replace('-', '_').replace(' ', '_')
        column_definitions = ', '.join([f"`{header}` {data_type}" for header, data_type in zip(headers, data_types)])
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({column_definitions})"
        cursor.execute(create_table_query)
       
        # Prepare for data insertion
        insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{header}`' for header in headers])}) VALUES ({', '.join(['%s' for _ in headers])})"
        
        # Reset file pointer and skip header
        csvfile.seek(0)
        next(reader)
        
        # Insert data rows
        for row in reader:
            cursor.execute(insert_query, row)
        
        connection.commit()

    cursor.close()
    connection.close()

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    app.run(debug=True)


