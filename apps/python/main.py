from flask import Flask,request,jsonify
from datetime import datetime,date
import re
import psycopg2

DB_HOST = 'localhost'
DB_NAME = 'hello_db'
DB_USER = 'hello_user'
DB_PASSWORD = 'hello_pass'
USERNAME_PATTERN = r'^[a-zA-Z]+$'
conn = psycopg2.connect(host=DB_HOST,dbname=DB_NAME,user=DB_USER,password=DB_PASSWORD)
cur = conn.cursor()
app = Flask(__name__)


def validate_username(username):
    return re.match(USERNAME_PATTERN,username) is not None


@app.route('/hello/<username>',methods=['PUT'])
def save_user_data(username):
    if not validate_username(username):
        return jsonify(error='Invalid username'),400
    try:
        dob = datetime.strptime(request.json['dateOfBirth'],'%Y-%m-%d').date()
    except (KeyError,ValueError):
        return jsonify(error='Invalid date of birth'),400
    if dob > date.today():
        return jsonify(error='Date of birth must be before today'),400
    cur.execute(
        'INSERT INTO users (username, dob) VALUES (%s, %s) ON CONFLICT (username) DO UPDATE SET dob = EXCLUDED.dob',
        (username,dob))
    conn.commit()
    return jsonify(message='User data saved successfully')


@app.route('/hello/<username>',methods=['GET'])
def get_hello_message(username):
    if not validate_username(username):
        return jsonify(error='Invalid username'),400
    cur.execute('SELECT dob FROM users WHERE username = %s',(username,))
    result = cur.fetchone()
    if result is None:
        return jsonify(error='User not found'),404
    dob = result[0]
    next_birthday = datetime(date.today().year,dob.month,dob.day).date()
    if next_birthday < date.today():
        next_birthday = datetime(date.today().year + 1,dob.month,dob.day).date()
    days_to_birthday = (next_birthday - date.today()).days
    if days_to_birthday == 0:
        message = f'Hello, {username}! Happy birthday!'
    else:
        message = f'Hello, {username}! Your birthday is in {days_to_birthday} day(s)'
    return jsonify(message=message)


if __name__ == '__main__':
    app.run(debug=True)
