import sqlite3
from flask import Flask, g, redirect, request, render_template, session, url_for
from flask_bootstrap import Bootstrap

DATABASE = 'app.db'
DEBUG = True
SECRET_KEY = 'b026Hzy4f9YMT14uS<*46T0opO9x7%'

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)
  
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_req ():
    g.db = connect_db()

@app.teardown_request
def tear_req(exception):
    if hasattr(g, 'db'):
        g.db.close()
    
@app.route('/')
def index():
    return render_template('login.html')
      
@app.route('/profile/<user>', methods=['GET','POST'])
def profile(user):
    notes= g.db.execute("SELECT content from posts WHERE username=?", [user])
    return render_template('profile.html', notes=notes)

@app.route('/signin', methods=['POST'])
def getUser():
    un = request.form['username']
    pw = request.form['password']
    cur = g.db.execute("SELECT username FROM users WHERE username=? AND password=?", [un, pw])
    users = [dict(name=row[0]) for row in cur.fetchall()]
    if len(users) > 0:
      #session['user'] = user[0]
      #session['logged_in']= True
      return redirect(url_for('profile', user=un))
    else:
      return redirect(url_for('index'))
      
@app.route('/logout')
def logout():
    #session.pop('logged_in', None)
    #session.pop('user', None)
    return render_template('login.html');
    
@app.route('/register', methods=['POST'])
def register():
    un = request.form['username']
    pw = request.form['password']
    email = request.form['email_addr']
    photo = request.form['picture']
    g.db.execute("INSERT INTO users VALUES (?,?,?,?)", [un, pw, email, photo])
    g.db.commit()
    return redirect(url_for('profile', user=un))
    
@app.route('/profile/<username>/add/<content>', methods=['GET', 'POST'])
def add(username, content):
    g.db.execute("INSERT INTO posts (username,content) Values(?,?)", [username, content])
    g.db.commit()
    return redirect(url_for('profile', user=username));
    
@app.route('/profile/note-remove', methods=['POST'])
def remove_note(username, content):
    g.db.execute("DELETE FROM posts WHERE username=? AND content=?", [username, content])
    g.db.commit()
    return redirect(url_for('profile', user=username));

@app.route('/profile/<username>/deleteMe')
def delete_acct(username):
    g.db.execute("DELETE FROM users WHERE username=?", [username])
    g.db.commit()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='magnusb.net')
