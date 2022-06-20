
from unittest import result
from flask_app.config.mysqlconnection import MySQLConnection,connectToMySQL
from flask_app import app
from flask_app.models import recipe
from flask import flash,session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 



class User:
    DB='recipes_schema'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password=data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes=[]

    #CREATE ----SQL----MODELS
    #create--> now will be diffrent , first will validate then will run query for creating user
    @classmethod
    def create_new_user(cls,data):
        # if the validation method on bottom returns true so , will stay inside function and create a user
        #if it returns false thats mean will flash the message and do not run the query.
        if not cls.validate_user_reg_data(data):
            # print("I am not valid data ^^^^^^^^^^^^^^^^^^") #refrence to see how my data looks like
            return False
        #if the validate function came true so all the inserted info are correct , so go a head and create new user.
        else:#befor run our query we have to hash our password so when we insert it , it will go hashed to db, so will do it in another static method with def called parsed_regestraion data to make our code clean and call it here.
            # print("&&&&&&&&&&&&&&&&&&&& is this data valide I'm on line 34")#refrence to see how my data looks like
            data=cls.parse_regestration_data(data)#we parsed our data that came from form by calling parsed data method  and will use it to create user now 
            query="""INSERT INTO users (first_name,last_name,email,password)
            VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)
            ;"""
            #running this query will give us user id so I called the variable user_id to be more descriptive
            user_id=connectToMySQL(cls.DB).query_db(query,data)
            # print("&&&&&&&&",user_id)
            #when we create an account we expext to login, so in this case we need to store user_id into session
            session['user_id']=user_id
            return user_id
            #after creating new user now its ti,e to go to controller.

    #READ ----SQL----MODELS
    # get_one user by email to make sure if the email already in use or not
    @classmethod
    def get_user_by_email(cls,email):
        data={
            'email':email
        }
        query="""
        SELECT * FROM users WHERE email=%(email)s
        ;"""
        result=connectToMySQL(cls.DB).query_db(query,data)#this result will come back with dictionary with key email and value of inserted email
        if result:# if the result came with value of inserted email then:
            result=cls(result[0])#then bring this data and pass it to class User and create instances from these data and in this case case will be false so, go and run flash message in validate method on bottom and call this function there.
        return result


    #GET USER BY ID WILL HELP US TO DISPLAY THE NAME IN DASHBOARD
    @classmethod
    def get_user_by_id(cls,data):
        query="""
        SELECT * FROM users WHERE id=%(id)s
        ;"""
        result=connectToMySQL(cls.DB).query_db(query,data)
        return cls(result[0])


    @classmethod
    def get_recipes_by_this_user(cls,data):
        query="""
        SELECT * FROM users 
        LEFT JOIN recipes
        ON users.id=recipes.user_id
        WHERE users.id=%(id)s
        ;"""
        result=connectToMySQL(cls.DB).query_db(query,data)
        print("&&&&&&&&&&&&&&&&&&&& result",result)
        this_user=cls(result[0])
        print("mmmmmmm",this_user)
        for row in result:
            data={
                'id':row['recipes.id'],
                'name':row['name'],
                'description':row['description'],
                'instruction':row['instruction'],
                'date_made':row['date_made'],
                'under_30_min':row['under_30_min'],
                'created_at':row['recipes.created_at'],
                'updated_at':row['recipes.updated_at']
            }
            this_user.recipes.append(recipe.Recipe(data))
        return this_user





#static method for valdiation USER
    @staticmethod
    def validate_user_reg_data(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #this regulaer exp for making sure the email must have charecters like letters and @ nd dot ...etc
        PASSWORD_REGEX=re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')#this regular exp for making sure the password must has one uppercase and one lower and one number
        is_valid = True # we assume this is true
        #validate our email to see if its in correct format
        if not EMAIL_REGEX.match(data['email']):
            flash("Use a real email")
            is_valid=False
        #validate email adress again to make sure it is not already used, this is done by using query select * from users where users.email=email
        #will go up and create class methode get_user_by_email()... for selecting users by email if it comes with email we will flash error message here , if it comes empty thats mean no error , go and create email
        # now after creating get _user_by_email method will call it here if the result came true.
        if User.get_user_by_email(data['email'].lower()):#lower function here for preventing duplicate emails if we insert by mistake uppercase and lower case , so in this case all leteeres will converted to uppercase.
            flash("Email already in use, insert another email adress")
            is_valid=False
        #validat first_name to make sure it is more than 3 chareters
        if len(data['first_name']) < 2:
            flash("first_Name must be at least 3 or more characters.")
            is_valid = False
        #validata last_name to make sure it is 3 charecters or more than 3 chareters
        if len(data['last_name']) < 2:
            flash("last_name must be at least 3 or more characters.")
            is_valid = False
        #validate password to make sure its more than 8 charecters
        if len(data['password'])<8:
            flash("your password must contain at least 2 charecters")
            is_valid=False
        #validate password again to make sure it matches the confirm password
        if data['password']!=data['confirm_password']:
            flash("passord do not match")
            is_valid=False
        #validate password to make sure the password must has one uppercase and one lower and one number
        if not PASSWORD_REGEX.match(data['password']):
            flash("password should contains at least one uppercase and one lowercase and one number")
            is_valid=False
        return is_valid

        #after finishing validating all user info now its time to create our user and in this case we need to create class method on the top .


#static method for parsed data to hashed our password (the data coming from form are plain as we inserted and to hash the password before passing it to db ,we need to hash it so, it will appear as a random charecters in db , to do so will create pased function with parsed empty dictionary like below:)
    @staticmethod
    def parse_regestration_data(data):
        parsed_data={}
        parsed_data['email']=data['email'].lower()#the data I give you find the key and set its value
        parsed_data['password']=bcrypt.generate_password_hash(data['password'])
        parsed_data['first_name']=data['first_name']
        parsed_data['last_name']=data['last_name']
        return parsed_data
        #now we have to go to top and call this function to hash password before creating user
        
    #method for login
    @staticmethod
    def login(data):
        # will check if the email came from db so we will check if the password matches 
        user=User.get_user_by_email(data['email'].lower())
        if user :
            if bcrypt.check_password_hash(user.password,data['password']):
                session['user_id']=user.id#store the user id that came with email into session
                return True
        #if no thing back from method get_user_by_email:
        flash("invalid either email adress or password")
        return False

