from flask import Flask, render_template, request, redirect, jsonify, url_for, flash


from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, UploadFile, User, Category, Project

# NEW IMPORTS FOR AUTHENTICATION
from flask import session as login_session
import random
import string
from datetime import datetime

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///woodworking_projects.db')
Base.metadata.bind = engine

# CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
#     'web']['client_id']

# Create anti-forgery state token


# @app.route('/login')
# @app.route('/gconnect', methods=['POST'])
# # DISCONNECT - Revoke a current user's token and reset their login_session
# @app.route("/gdisconnect")


# SHOW CATEGORIES:
@app.route('/')
@app.route('/category')
def showCategories():
    # return "This page will display all restaurants"
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).outerjoin(UploadFile).all()
    return render_template('categories.html', categories=categories)


# ADD CATEGORY:
@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newCategory = Category(
            CategoryName=request.form['name'])
        session.add(newCategory)
        session.commit()
        # flash("New Category Created!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('newcategory.html')


# # EDIT CATEGORY:
@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedCategory = session.query(
        Category).filter_by(CategoryID=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.CategoryName = request.form['name']
        session.add(editedCategory)
        session.commit()
        # flash("Category Successfully Edited!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('editcategory.html', category_id=category_id, category=editedCategory)


# DELETE CATEGORY:
@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deletedCategory = session.query(
        Category).filter_by(CategoryID=category_id).one()
    if request.method == 'POST':
        session.delete(deletedCategory)
        session.commit()
        flash("Category Successfully Deleted!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('deletecategory.html', category=deletedCategory)


# SHOW PROJECTS:
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/projects')
def showProjects(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(
        Category).filter_by(CategoryID=category_id).one()
    projects = session.query(Project).filter_by(
        CategoryID=category.CategoryID)
    return render_template('projects.html', category=category, projects=projects)


# ADD PROJECT:
@app.route('/category/<int:category_id>/projects/new', methods=['GET', 'POST'])
def newProject(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newProject = Project(
            ProjectName=request.form['name'], ProjectDesc=request.form['description'],
            CategoryID=category_id, DateAdd=datetime.now(), DateEdit=datetime.now())
        session.add(newProject)
        session.commit()
        # flash("New Project Created!")
        return redirect(url_for('showProjects', category_id=category_id))
    else:
        return render_template('newproject.html', category_id=category_id)


# # EDIT PROJECT:
@app.route('/category/<int:category_id>/projects/<project_id>/edit', methods=['GET', 'POST'])
def editProject(category_id, project_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedProject = session.query(Project).filter_by(
        ProjectID=project_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedProject.ProjectName = request.form['name']
            editedProject.ProjectDesc = request.form['description']
            editedProject.DateEdit = datetime.now()
            # editedProject.price = request.form['price']
        session.add(editedProject)
        session.commit()
        flash("Project Successfully Edited!")
        return redirect(url_for('showProjects', category_id=category_id))
    else:
        return render_template('editproject.html', category_id=category_id, project_id=project_id, project=editedProject)


# # DELETE PROJECT:
@app.route('/category/<int:category_id>/projects/<project_id>/delete', methods=['GET', 'POST'])
def deleteProject(category_id, project_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deletedProject = session.query(
        Project).filter_by(ProjectID=project_id).one()
    if request.method == 'POST':
        session.delete(deletedProject)
        session.commit()
        flash("Project Successfully Deleted!")
        return redirect(url_for('showProjects', category_id=category_id))
    else:
        return render_template('deleteproject.html', category_id=category_id, project_id=project_id, project=deletedProject)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
