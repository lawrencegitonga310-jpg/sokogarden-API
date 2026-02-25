# import flask and its components
from flask import*
import os

# import a  pymysql module it helps to create a connection btn python flask and mysql database
import pymysql

# crate a flask application
app = Flask(__name__)

# configure the location where your Products images will be saved on your application
app.config["UPLOAD_FOLDER"]="static/images"

# below is the signup route(registration)
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

@app.route("/api/signin",methods=["POST"])
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
        sql ="SELECT* FROM users WHERE email=%s AND password=%s"
        
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

 # below is a route for adding products
@app.route("/api/add_products",methods=["POST"])
def add_products():
    if request.method == "POST":
        # extract the data entered on the form 
        product_name =request.form["product_name"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        # for the product photo we shall fetch it from the file as shown below
        product_photo =request.files["product_photo"]

        # extract the the file name of the product photo
        filename= product_photo.filename
        # by use of os module we can extract the file path where the images is currently saved
        photo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        
        # print("this is the photo path:",photo_path)
        # save the product phot image into the new location
        product_photo.save(photo_path)

        # print them out to test whether you are receiving the details sent with the request
        # print(product_name, product_description, product_cost, product_photo) 

        # establish a connection to the db
        connection = pymysql.connect(host="localhost", user="root", password= "", database= "sokogardenonline")

        # create cursor
        cursor = connection.cursor()

        # structure the sql query to insert the product details to the database
        sql = "INSERT INTO product_details(product_name, product_description, product_cost, product_photo) VALUES (%s,%s,%s, %s)"
       
      #  create a tuple that will hold the data from which are current held onto the different variables declared
    data = (product_name, product_description, product_cost, filename)

    # use the cursor to execute the sql as you replace the placeholders with the actual data
    cursor.execute(sql, data)

    # commit the changes to database 
    connection.commit()


    return jsonify({"message" : "Add product route accessed"})
    
# below is a route for fetching products
@app.route("/api/get_products")
def get_products():
    # create a connection to db 
   connection = pymysql.connect(host="localhost", user="root", password= "", database= "sokogardenonline")

    # create a cursor
   cursor= connection.cursor()

  # structure the query to fetch all the products from the table products_details
   sql = "SELECT * FROM product_details"


# execute the query
   cursor.execute(sql)

# create a variable that hold the data fetched from the table
   products = cursor.fetchall()





   return jsonify(products)



# run the web app
app.run(debug=True)

