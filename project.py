from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# NEW IMPORTS FOR AUTHENTICATION
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']


# Create anti-forgery state token
@app.route('/login')
@app.route('/gconnect', methods=['POST'])
# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route("/gdisconnect")
# SHOW CATEGORIES:
@app.route('/')
@app.route('/category')
def showCategories():
    # Module Code Here

    # ADD CATEGORY:


@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    # EDIT CATEGORY:


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory():
    # DELETE CATEGORY:


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory():
    # SHOW PROJECTS:


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/projects')
def showProjects():
    # ADD PROJECT:


@app.route('/category/<int:category_id>/projects/new', methods=['GET', 'POST'])
def newProject():
    # EDIT PROJECT:


@app.route('/category/<int:category_id>/projects/<project_id>/edit', methods=['GET', 'POST'])
def editProject():
    # DELETE PROJECT:


@app.route('/category/<int:category_id>/projects/<project_id>/delete', methods=['GET', 'POST'])
def deleteProject():
