import sqlite3
from flask import Flask, flash, g, redirect, request, render_template, session, url_for
from datetime import datetime
from flask_bootstrap import Bootstrap 

DATABASE = 'app.db'
DEBUG = True
SECRET_KEY = 'b026Hzy4f9YMT14uS<*46T0opO9x7%'


app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)

#connect to database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#default session variables
def setSession():
    session['logged_in']=False
    session['user'] = None
  
#add a new user
def addUser(username, password, email):
    cur = g.db.execute("SELECT username FROM Users WHERE username=? OR email=?", [username, email])
    userCheck = [dict(un=row[0]) for row in cur.fetchall()]
    if len(userCheck) > 0:
        return False;
    else:
        g.db.execute("INSERT INTO Users Values(?,?,?,?)", [username, password, email, 0])
        g.db.commit()
        user = {"name":username, "posts":0}
        session['user'] = user
        return True;

#add a user post to the database
def add_Post(content):
    g.db.execute("INSERT INTO Posts Values(?,?,?,?,?,?)", [session['user']['posts']+1, session['user']['name'], content, "", 0, 0])
    g.db.commit()
    session['user']['posts'] += 1

#remove user from the database
def rem_user():
    g.db.execute("DELETE FROM Users WHERE username=?", ([session['user']['name']]))
    g.db.execute("DELETE FROM Posts WHERE poster=?", ([session['user']['name']]))
    g.db.execute("DELETE FROM Listens WHERE speaker=? OR listener=?", [session['user']['name'], session['user']['name']])
    g.db.execute("DELETE FROM Praises WHERE poster=?", ([session['user']['name']]))
    g.db.execute("DELETE FROM Comments WHERE username=?", ([session['user']['name']]))
    g.db.commit()

#remove a post from the database
def rem_post(ID):
    g.db.execute("DELETE FROM Posts WHERE ID=? and poster=?", [ID, session['user']['name']])
    g.db.commit()
    
#get user information from database
def getUser(username, password):
    cur = g.db.execute("SELECT username, posts FROM Users WHERE username=? AND password=?", [username, password])
    user = [dict(name=row[0], posts=row[1]) for row in cur.fetchall()]
    if len(user) < 1:
        return []
    else:
        return user[0]

#get user posts to display on profile
def getPosts():
    cur = g.db.execute("SELECT * from posts WHERE poster=?", [session['user']['name']])
    posts = [dict(ID=row[0], poster=row[1], content=row[2], date=row[3], praises=row[4], comments=row[5]) for row in cur.fetchall()]
    if len(posts) < 1:
        return []
    else:
        return posts

    
#open database for each request
@app.before_request
def before_req ():
    g.db = connect_db()

#close database after each request
@app.teardown_request
def tear_req(exception):
    if hasattr(g, 'db'):
        g.db.close()
     
##################################
# Initial Login and Registration #
##################################
    
#load login/register screen
@app.route('/')
def index():
    setSession()
    return redirect(url_for('login'))

#Check if user is already logged in
@app.route('/login')
def login():
    if session['logged_in'] == False:
       return render_template('login.html')
    else:
       return redirect('profile')
          
#sign in for an existing user
@app.route('/signin', methods=['POST'])
def sign_in():
    un = request.form['username']
    pw = request.form['password']
    session['user'] = getUser(un, pw)
    if session['user'] != []:
      session['logged_in'] = True 
      return redirect(url_for('profile'))
    else:
      return redirect(url_for('login'))
      
#logout of user account
@app.route('/logout')
def logout():
    g.db.execute("UPDATE Users SET posts=? WHERE username=?", [session['user']['posts'], session['user']['name']])
    setSession()
    return redirect(url_for('login'));

#Register new user
@app.route('/register', methods=['POST'])
def reg():
    un = request.form['regUN']
    pw = request.form['regPass']
    email = request.form['email_addr']
    if addUser(un, pw, email) == True:
      return redirect(url_for('profile'))
    else:
      return redirect(url_for('login'))
      
#################################
#  Profile Display and Options  #
#################################

#Load Profile    
@app.route('/profile')
def profile():
    posts = getPosts()
    return render_template('profile.html', posts=posts)
        
#Add post
@app.route('/profile/add_post', methods=['POST'])
def post():
    content = request.form['newPost']
    add_Post(content)
    return redirect(url_for('profile'))

#Delete account
@app.route('/profile/delete')
def remUser():
    rem_user()
    setSession()
    return redirect(url_for('login'))

#Delete post
@app.route('/profile/remPost/<postID>')
def remPost(postID):
    rem_post(postID)
    return redirect(url_for('profile', user=session['user']))

#run application
if __name__ == '__main__':
    app.run(host='magnusb.net')
