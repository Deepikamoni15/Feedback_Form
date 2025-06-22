from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask import Flask,flash

app = Flask(__name__)

# Initialize MySQL
def init_mysql(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'FeedbackDB'

    mysql = MySQL(app)
    return mysql

mysql = init_mysql(app)

# Secret key for flash messages
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    feedback = request.form['feedback']
    rating = request.form['rating']

    # Insert feedback into MySQL database
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feedback (name, email, feedback, rating) VALUES (%s, %s, %s, %s)", 
                    (name, email, feedback, rating))
        mysql.connection.commit()
        cur.close()
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('thank_you', name=name))
    except Exception as e:
        flash('Error submitting feedback: ' + str(e), 'danger')
        return redirect(url_for('home'))

@app.route('/thank_you/<name>')
def thank_you(name):
    return render_template('thank_you.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)

