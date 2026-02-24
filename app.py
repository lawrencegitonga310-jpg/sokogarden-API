# import flask and its components
from flask import*

# import a  pymysql module it helps to create a connection btn python flask and mysql database
import pymysql

# crate a flask application
app = Flask(__name__)


# below is the signup route
@app.route("/api/signup",methods=["POST"])
def signup():
     if request.method=="POST":
        # Extract the different details entered on the form
        username= request.form["username"]
        email= request.form["email"]
        password= request.form["password"]
        phone = request.form["phone"]

          #  by the use of print function let print those details
         # print(username,email,password,phone)

          # establish a connection between flask/python and mysql
        connection = pymysql.connect(host="localhost", user="root", password="",database="sokogardenonline")

          # create a cursor to execute the sql queries
        cursor= connection.cursor()

          # structure an sql to insert the details received from the form
          # the %s is a place holder -Aplaceholder it stands in a place of actual value ie we shall replace them later on  
        sql ="INSERT INTO users(username,email,phone,password)VALUES(%s,%s,%s,%s)"

          # create a taple that will hold the data gotten from the form
        data =(username,email,phone,password)

          # by the use of the cursor execute the sql as you replace the placeholder with the actualvalue
        cursor.execute(sql,data) 

            # commit the changes to the database
        connection.commit()

     return jsonify({"message":"User register successfully"})

@app.route("/api/signup",methods=["POST"])
def signin():
     if request.method=="POST":
        #  extract the two details entered on the form
        email= request.form["email"]
        password= request.form["password"]

        # print the details entered
        # print(email,password)

        # create/establish A connection to the database
        connection = pymysql.connect(host="localhost", user="root", password="",database="sokogardenonline")

        # create a cursor 
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # structure the sql query that will check if the email and password entered are correct
        sql ="SELECT* FROM users WHERE email=%s AND password=%s)"
        
        # Put the data received from the form into a tuple
        data = (email,password)

        # by the use of the cursor execute the sql
        cursor.execute(sql, data)

        # check wheather there are row returned and store the same on a variable
        count =cursor.rowcount
        # print(count)

        # if there are records returned it means the password and email entered are correct otherwise it means they are wrong
        if count == 0:
          return jsonify({"message":"login failed"})
        else:
            # there must be a user so we create a variable that will hold the details of the user fetched from the database
            user=cursor.fetchone()
            # return the details to the fronted as well as a message
            return jsonify({"message":"User logged in successfully", "user":user})

        
# run the web app
app.run(debug=True)

