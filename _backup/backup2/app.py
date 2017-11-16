from flask import Flask, render_template, request, jsonify
import sqlite3
# Add AJAX to be able to do live update of variables. Such as the status of 'result' of the quiz

app = Flask(__name__)


#create and connect to database
DATABASE = 'myapp.db'
def connect_db():
    return sqlite3.connect(DATABASE)


#create index url & function mapping for root or / (index page)
@app.route('/')
def index():
    db = connect_db()
    cur = db.execute('select id, myname, country_of_residence, english from people')
    entries = [dict(id = row[0], myname = row[1], country_of_residence = row[2], english = row[3]) for row in cur.fetchall()]
    print(entries)
    db.close()
    return render_template('ProfileList.html', entries = entries)

#create routing for myProfile
@app.route('/myprofile')
def showmyprofile():
    return render_template('MyProfile.html')

#create mapping to show the form for /addprofile
@app.route('/addprofileform')
def addprofileform():
    return render_template('MyProfileForm.html')

#create a mapping for /addprofile
@app.route('/addprofile')
def addprofile():
    myname = request.args.get('myname')
    country_of_residence = request.args.get('country_of_residence')
    db = connect_db()
    sql = 'insert into people (myname, country_of_residence) values (?,?)'
    db.execute(sql, [myname, country_of_residence])
    db.commit()
    db.close()
    return render_template('MyProfile.html', myname = myname, country_of_residence = country_of_residence)

#update profile
@app.route('/editprofile')
def editprofile():
    id = request.args.get('id')
    db = connect_db()
    cur = db.execute('select id, myname, country_of_residence, english from people where id=?',[id])
    rv = cur.fetchall()
    cur.close()
    person = rv[0]
    print(rv[0])
    db.close()
    return render_template('MyProfileUpdateForm.html', person=person)

#update profile
@app.route('/updateprofile')
def updateprofile():
    id = request.args.get('id')
    myname = request.args.get('myname')
    country_of_residence = request.args.get('country_of_residence')
    db = connect_db()
    sql = 'update people set myname=?, country_of_residence=? where id=?'
    db.execute(sql, [myname,country_of_residence,id])
    db.commit()
    db.close()
    return index()

#This functions prints transmits the data from the SQL DB
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    id = request.args.get('id')
    db = connect_db()
    cur = db.execute('select id, myname, country_of_residence from people where id=?',[id])
    rv = cur.fetchall()
    cur.close()
    person = rv[0]
    print(rv[0])
    db.close()
    return render_template('Quiz_new.html', person=person)

# #THIS IS TO BE DELETED
# @app.route('/validate', methods=['GET', 'POST'])
# def _validate():
#     #article = request.args.get('article')
#     id = request.args.get('id')
#     article = request.args.get('proglang')
#     print(article, id)
#     db = connect_db()
#     cur = db.execute('select id, myname, country_of_residence, english from people where id=?', [id])
#     rv = cur.fetchall()
#     cur.close()
#     person = rv[0]
#     print('this is :',rv[0])
#     db.close()
#     #a = '<a href="/">Go back to WordList</a>'
#     if article.lower() == person[1]:
#         result = 'Correct'
#     else:
#         result = 'Wrong'
#     return jsonify(result=result)#result +' <br/> <br/> '# + a

#This func validates the answer of the user
@app.route('/_validate', methods=['GET', 'POST'])
def validate():
    id = request.args.get('id')
    article = request.args.get('article')
    english = request.args.get('english')
    res = request.args.get('res')
    print("here are some values kyyyk :",id, article, res, english)
    #article = request.args.get('proglang')
    #print('id herererer',id)
    db = connect_db()
    cur = db.execute('select id, myname, country_of_residence, english from people where id=?', [id])
    rv = cur.fetchall()
    cur.close()
    person = rv[0]
    #print('this is :',rv[0])
    db.close()
    #a = '<a href="/">Go back to WordList</a>'
    if article.lower() == person[1] and english.lower() == person[2]:
        result = '<span style="color: #33cc33;">CORRECT</span>'
    elif article.lower() == person[1] and english.lower() != person[2]:
        result = '<span style="color: #ff0000;">WRONG WORD</span>'
    elif article.lower() != person[1] and english.lower() == person[2]:
        result = '<span style="color: #ff0000;">WRONG ARTICAL</span>'
    else:
        result = '<span style="color: #ff0000;">WRONG</span>'
    return jsonify(result=result)

# #Button on QUIZ PAGE
# @app.route('/interactive', methods = ['GET', 'POST'])
# def interactive():
#     article = request.args.get('article')
#     id = request.args.get('id')
#
# #feeds Javascript to return the result
# @app.route('/background_process')
# def background_process():
# 	try:
# 		lang = request.args.get('article', 0, type=str)
# 		if lang.lower() == 'python':
# 			return jsonify(result='You are wise')
# 		else:
# 			return jsonify(result='Try again.')
# 	except Exception as e:
# 		return str(e)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    # try:
    #     PORT = int(os.environ.get('SERVER_PORT', '5555'))
    # except ValueError:
    #     PORT = 5555
    # app.run(HOST, PORT)

    app.run(host='0.0.0.0')