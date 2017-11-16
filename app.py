from flask import Flask, render_template, request, jsonify, json
import sqlite3, datetime
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
    cur = db.execute('select id, myname, english from people')
    entries = [dict(id = row[0], myname = row[1], english = row[2]) for row in cur.fetchall()]
    db.close()
    return render_template('ProfileList.html', entries = entries)

#get all user's answers
@app.route('/_answerspage', methods=['GET', 'POST'])
def readAnswers():
#this is the list with all the answers; The dictionary contains the index + answers;
    answers = json.loads(request.args.get('tmpAns'))
    print('answer here: ', answers[1], '   |||    the ful list of answers', answers)
# get database values
    db = connect_db()
    cur = db.execute('select id, myname, english from people')
    entries = [dict(id=row[0], myname=row[1], english=row[2]) for row in cur.fetchall()]
    #print('entries here: ',entries) # this is the dictionary with keys: id, myname, english
    #print('1: ', entries[1]['id'])
    db.close() # don't close the database!
#append answers and database values into the same dictionary
    for i in range(len(answers)):
        if answers[i] == entries[i]['myname']:
            entries[i]['answer'] = answers[i]
            entries[i]['correct'] = 'yes'
        else:
            entries[i]['answer'] = answers[i]
            entries[i]['correct'] = 'no'
    print('Final list here: ',entries) # check how the dictionary looks like
    #jsonify(entries)
    return render_template('AnswersList.html', entries=entries) #entries=entries)

    #return jsonify(entries=entries)

#get all user's answers
@app.route('/_answerspage2', methods=['GET','POST'])
def readAnswers2():

  # this is the list with all the answers; The dictionary contains the index + answers;
    answers = request.args.getlist('dutch[]')
    print('andswers HERE: ', answers)
    print('answer here: ', answers[0], '   |||    the ful list of answers', answers)
  # get database values
    db = connect_db()
    cur = db.execute('select id, myname, english from people')
    entries = [dict(id=row[0], myname=row[1], english=row[2]) for row in cur.fetchall()]
    db.close()  # don't close the database!
    #if request.method == 'POST':
    for i in range(len(answers)):
        if answers[i] == entries[i]['myname']:
            entries[i]['answer'] = answers[i]
            entries[i]['correct'] = '''<span style="color: #33cc33;">CORRECT</span>'''
        else:
            entries[i]['answer'] = answers[i]
            entries[i]['correct'] =  '''<span style="color: #ff0000;">WRONG</span>'''
    print('Final list here: ', entries)  # check how the dictionary looks like
  #  jsonify(entries)
    return render_template('AnswersList.html', entries=entries)  # entries=entries)

#create routing for myProfile
@app.route('/myprofile')
def showmyprofile():
    return render_template('MyProfile.html')

#create mapping to show the form for     /addprofile
@app.route('/addprofileform')
def addprofileform():
    return render_template('MyProfileForm.html')

#create a mapping for /addprofile
@app.route('/addprofile')
def addprofile():
    myname = request.args.get('myname')
    english = request.args.get('english')
    db = connect_db()
    sql = 'insert into people (myname, english) values (?,?)'
    db.execute(sql, [myname, english])
    db.commit()
    db.close()
    return render_template('MyProfile.html', myname = myname, english = english)

#update profile
@app.route('/editprofile')
def editprofile():
    id = request.args.get('id')
    db = connect_db()
    cur = db.execute('select id, myname, english from people where id=?',[id])
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
    english = request.args.get('english')
    db = connect_db()
    sql = 'update people set myname=?, english=? where id=?'
    db.execute(sql, [myname,english,id])
    db.commit()
    db.close()
    return index()

#This func validates the answer of the user
@app.route('/_validate', methods=['GET', 'POST'])
def validate():
    id = request.args.get('id')
    #article = request.args.get('article')
    english = request.args.get('english')
    res = request.args.get('res')
    print("here are some values kyyyk :",id, res, english)
    #article = request.args.get('proglang')
    #print('id herererer',id)
    db = connect_db()
    cur = db.execute('select id, myname, english from people where id=?', [id])
    rv = cur.fetchall()
    cur.close()
    person = rv[0]
    #print('this is :',rv[0])
    db.close()
    #a = '<a href="/">Go back to WordList</a>'
    if english.lower() == person[1]:
        result = '<span style="color: #33cc33;">CORRECT</span>'
    else:
        result = '<span style="color: #ff0000;">WRONG</span>'
    return jsonify(result=result)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    # try:
    #     PORT = int(os.environ.get('SERVER_PORT', '5555'))
    # except ValueError:
    #     PORT = 5555
    # app.run(HOST, PORT)

    app.run(host='0.0.0.0')


