from flask import Flask , request
import mysql.connector
import json
from flask_cors import CORS, cross_origin

import  etudiant


app = Flask(__name__)
cors = CORS(app)


mydb = mysql.connector.connect(
    host="localhost", user="root",
    password="",
    database="ensi"
                                )

# web methods
@app.route('/') # annotation
def hello_world():  # put application's code here
    return 'Hello student backend'

@app.route('/savestudent' , methods=['POST']) # annotation
def savestudent():  # put application's code here
    # Jaon object Front end
    args = request.json

    #print(args)

    et = etudiant.Etudiant(args.get('nom') ,args.get('age') , args.get('note'))
    # cursor temp
    mycursor = mydb.cursor()
    # prepared statement
    # mappig param relation
    sql = "insert into etudiant (nom , age , note) value (%s , %s , %s)"
    val = (et.nom, et.age ,et.note)

    mycursor.execute(sql, val)
    # declancher la transaction physique
    mydb.commit()

    return 'Succes student'


@app.route('/getstudents') # annotation
def getstudents():  # put application's code here
    malist = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM etudiant")
    myresult = mycursor.fetchall()
    for x in myresult:
        malist.append(etudiant.Etudiant(x[1] ,x[2] , x[3]).__dict__)
        #print(x[2])

    return malist

if __name__ == '__main__':
    app.run(host="127.0.0.1" , port=5000 , debug=True)
