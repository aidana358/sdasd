from flask import Flask, render_template, request, redirect, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'aaaaaaaa'

conn = psycopg2.connect(
    dbname="database",
    user="postgres",
    password="963600zx",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login_input = request.form['login']
        password_input = request.form['password']

        cur.execute("SELECT * FROM site_users WHERE login = %s AND password = %s", (login_input, password_input))
        user = cur.fetchone()

        if user:
            if login_input == 'admin' and password_input == '12345':
                session['user'] = login_input
                return redirect('/welcome')
            else:
                return redirect('/no_access')
        else:
            return redirect('/no_access')

    return render_template('login.html', error=error)


@app.route('/welcome')
def welcome():
    if 'user' not in session:
        return redirect('/login')
    return render_template('welcome.html', login=session['user'])


@app.route('/no_access')
def no_access():
    return render_template('no_access.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
