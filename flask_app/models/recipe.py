from flask_app.config.mysqlconnection import MySQLConnection,connectToMySQL
from flask_app import app
from flask import flash,session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 


class Recipe:
    DB='recipes_schema'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_made = data['date_made']
        self.under_30_min = data['under_30_min']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    #create
    @classmethod
    def create_new_recipe(cls,data):
        if not cls.validate_user_rcipe(data):
            # print("I am not valid data ^^^^^^^^^^^^^^^^^^") #refrence to see how my data looks like
            return False
        else:
            query="""INSERT INTO recipes (name,description,instruction,date_made,under_30_min,user_id)
            VALUES (%(name)s,%(description)s,%(instruction)s,%(date_made)s,%(under_30_min)s,%(user_id)s)
            ;"""
            result=connectToMySQL(cls.DB).query_db(query,data)
            return result

    #read

    @classmethod
    def get_recipe_by_id(cls,id):
        data={
            'id':id
        }
        query="""SELECT * FROM recipes WHERE id=%(id)s
        ;"""
        result=connectToMySQL(cls.DB).query_db(query,data)
        return cls(result[0])


    #update 
    @classmethod
    def update_recipe_by_id(cls,data):
        if not cls.validate_user_rcipe(data):
            # print("I am not valid data ^^^^^^^^^^^^^^^^^^") #refrence to see how my data looks like
            return False
        query="""
        UPDATE recipes SET name=%(name)s,description=%(description)s,instruction=%(instruction)s,date_made=%(date_made)s,under_30_min=%(under_30_min)s
        WHERE id=%(id)s
        ;"""
        result= connectToMySQL(cls.DB).query_db(query,data)
        print("5555555555555555",result)
        return result


    #delete

    @classmethod
    def delete_recipe_by_id(cls,id):
        data={
            'id':id
        }
        query="""
        DELETE FROM recipes WHERE id=%(id)s
        ;"""
        result=connectToMySQL(cls.DB).query_db(query,data)
        return result


#static method for valdiation Recipe
    @staticmethod
    def validate_user_rcipe(data):
        is_valid=True
        if len(data['name']) < 3:
            flash("Name must be at least 3 or more characters.")
            is_valid = False

        if len(data['instruction']) < 3:
            flash("instruction must be at least 3 or more characters.")
            is_valid = False
        if len(data['description'])<3:
            flash("description must be at least 3 or more characters")
            is_valid=False
        if  'under_30_min' not in data:
            flash("You must select Yes Or No")
            is_valid=False
        if  data['date_made']=="":
            flash("You must select date")
            is_valid=False
        return is_valid
