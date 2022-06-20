

from flask_app import app
from flask import render_template,redirect,request,session, flash
from flask_app.models import user,recipe

@app.route('/recipes/new')
def show_index():
    if 'user_id' in session:
        data={
        "id":session['user_id']
        }
        return render_template('new_recipe.html',this_user=user.User.get_user_by_id(data))

#create
@app.route('/create/recipe',methods=['POST'])
def create():
    if 'user_id' in session:
        if  recipe.Recipe.create_new_recipe(request.form):
            return redirect('/dashboard')
        return redirect('/recipes/new')

@app.route('/recipes/<int:id>')
def show_recipe_by_id(id):
    if 'user_id' in session:
        data={
        "id":session['user_id']
        }

    this_recipe=recipe.Recipe.get_recipe_by_id(id)
    return render_template('recipe_info.html',this_recipe=this_recipe,this_user=user.User.get_user_by_id(data))

@app.route('/delete/recipe/<int:id>')
def destroy_recipe(id):
    recipe.Recipe.delete_recipe_by_id(id)
    return redirect('/dashboard')



@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' in session:
        this_recipe=recipe.Recipe.get_recipe_by_id(id)
        return render_template('edit_recipe.html',this_recipe=this_recipe)
    return redirect('/logout')

@app.route('/recipes/update/<int:id>',methods=['POST'])
def submit_edit_recipe(id):
    data={
        'id':id,
        'name':request.form['name'],
        'description':request.form['description'],
        'instruction':request.form['instruction'],
        'date_made':request.form['date_made'],
        'under_30_min':request.form['under_30_min'],

    }
    if 'user_id' in session:
        if  recipe.Recipe.update_recipe_by_id(data)==None:
            return redirect('/dashboard')
        else:
            return redirect('/logout')





