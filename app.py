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

    
        







# run the application
app.run(debug=True)