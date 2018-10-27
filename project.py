from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   flash,
                   make_response)

from sqlalchemy import create_engine, asc, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, UploadFile, User, Category, Project

# NEW IMPORTS FOR AUTHENTICATION
from flask import session as login_session
import random
import string
from datetime import datetime
import os

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

engine = create_engine('sqlite:///woodworking_projects.db')
Base.metadata.bind = engine

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']


# Create a state token & store in session for later validation.


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps(
            'Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            'client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    login_session['provider'] = 'google'

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 50px; height: 50px;border-radius: 25px;'
    output += '-webkit-border-radius: 25px;-moz-border-radius: 25px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps(
            'Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    # Exchange client token for long-lived server-side token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_'
    url += 'exchange_token&'
    url += 'client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use tokent to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    # Strip expire tag from access token
    token = result.split(",")[0]
    token = token.split(":")[1]
    token = token.replace('"', '')
    print "Access Token: %s" % access_token
    print "Stripped Token: %s" % token

    url = 'https://graph.facebook.com/v2.8/me?'
    url += 'access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print "url sent for API access:%s" % url
    print "API JSON result: %s" % result
    data = json.loads(result)

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']
    login_session['provider'] = 'facebook'
    # login_session['picture'] = data['data']['url']

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me?'
    url += 'access_token=%s&fields=picture' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    print "Picture Data: %s" % data

    login_session['picture'] = data['picture']['data']['url']

    # See if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 50px; height: 50px;border-radius: 25px;'
    output += '-webkit-border-radius: 25px;-moz-border-radius: 25px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if login_session['picture'] is None or login_session['picture'] == "":
        defaultImage = "https://i1.wp.com/www.winhelponline.com/blog/"
        defaultImage += "wp-content/uploads/2017/12/user.png?"
        defaultImage += "fit=256%2C256&quality=100&ssl=1"
        newUser = User(Username=login_session['username'],
                       UserEmail=login_session['email'],
                       UserPicture=defaultImage)
    else:
        newUser = User(
            Username=login_session['username'],
            UserEmail=login_session['email'],
            UserPicture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(
        UserEmail=login_session['email']).first()
    return user.UserID


def getUserID(checkEmail):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        checkUser = session.query(User).filter_by(
            UserEmail=checkEmail).one()
        return checkUser.UserID
    except Exception:
        return None


def getUserInfo(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        userInfo = session.query(User).filter_by(UserID=user_id).one()
        return userInfo
    except Exception:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route("/gdisconnect")
def gdisconnect():
    # Only disconnect a connected user:
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token:
    # access_token = credentials.access_token
    print('In gdisconnect access token is %s' % access_token)
    print('Username is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('Result is')
    print(result)

    if result['status'] == '200':
        # Reset the user's session:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps(
            'Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbdisconnect')
def fbdisconnect():
    print "Facebook ID: %s" % login_session['facebook_id']
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']
    return "You have been logged out."


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()

        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCategories'))
    else:
        flash("You are not currently logged in.")
        return redirect(url_for('showCategories'))


# **************************************************************************
# SHOW CATEGORIES:
# **************************************************************************
@app.route('/')
@app.route('/category')
def showCategories():
    # return "This page will display all restaurants"
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    recentProjects = session.query(Project).outerjoin(
        Category).outerjoin(User).order_by(Project.DateAdd.desc()).limit(6)
    if 'username' not in login_session:
        return render_template('publiccategories.html', categories=categories,
                               recentProjects=recentProjects)
    else:
        return render_template('categories.html', categories=categories,
                               recentProjects=recentProjects)


# **************************************************************************
# ADD CATEGORY:
# **************************************************************************
@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        if request.files.get("picture") is not None:
            file = request.files.get("picture")
            filename = file.filename
            destination = "/".join([target, filename])
            file.save(destination)

            newCategory = Category(
                CategoryName=request.form['name'],
                CategoryPicture=filename,
                UserID=login_session['user_id'])
        else:
            newCategory = Category(
                CategoryName=request.form['name'],
                CategoryPicture='default.jpg',
                UserID=login_session['user_id'])
        session.add(newCategory)
        session.commit()
        flash("New Category Created!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('newcategory.html')


# **************************************************************************
# EDIT CATEGORY:
# **************************************************************************
@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedCategory = session.query(
        Category).filter_by(CategoryID=category_id).one()
    if editedCategory.UserID != login_session['user_id']:
        output = ""
        output += "<script>function myFunction() {alert('You are not "
        output += "authorized to edit this category. Please access one of "
        output += "the categories you created or create a new category "
        output += "in order to edit.'); window.location.href = '/';}"
        output += "</script><body onload='myFunction()''>"
        return output
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.CategoryName = request.form['name']
            target = os.path.join(APP_ROOT, 'static/images/')
            # if not os.path.isdir(target):
            #     os.mkdir(target)
            if request.files.get("picture") is not None:
                file = request.files.get("picture")
                filename = file.filename
                destination = "/".join([target, filename])
                file.save(destination)
                editedCategory.CategoryPicture = filename
            else:
                if editedCategory.CategoryPicture is None:
                    editedCategory.CategoryPicture = 'default.jpg'
        session.add(editedCategory)
        session.commit()
        flash("Category Successfully Edited!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('editcategory.html', category_id=category_id,
                               category=editedCategory)


# **************************************************************************
# DELETE CATEGORY:
# **************************************************************************
@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deletedCategory = session.query(
        Category).filter_by(CategoryID=category_id).one()
    if deletedCategory.UserID != login_session['user_id']:
        output = ""
        output += "<script>function myFunction() {alert('You are not "
        output += "authorized to delete this category. Please access one of "
        output += "the categories you created or create a new category in "
        output += "order to delete.'); window.location.href = '/';}"
        output += "</script><body onload='myFunction()''>"
        return output
    if request.method == 'POST':
        session.delete(deletedCategory)
        session.commit()
        flash("Category Successfully Deleted!")
        return redirect(url_for('showCategories'))
    else:
        return render_template('deletecategory.html', category=deletedCategory)


# **************************************************************************
# SHOW PROJECTS:
# **************************************************************************
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/projects')
def showProjects(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(
        Category).filter_by(CategoryID=category_id).one()
    contributor = getUserInfo(category.UserID)
    projects = session.query(Project).filter_by(
        CategoryID=category.CategoryID)
    if 'username' not in login_session:
        return render_template('publicprojects.html', category=category,
                               projects=projects)
    else:
        if contributor and contributor.UserID != login_session['user_id']:
            return render_template('publicprojects.html', category=category,
                                   projects=projects)
        else:
            return render_template('projects.html', category=category,
                                   projects=projects, contributor=contributor)


# **************************************************************************
# SHOW ONE PROJECT:
# **************************************************************************
@app.route('/category/<int:category_id>/projects/<int:project_id>')
def showOneProject(category_id, project_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(
        CategoryID=category_id).one()
    project = session.query(Project).filter_by(
        ProjectID=project_id).one()
    photos = session.query(UploadFile).filter_by(
        ProjectID=project_id).all()
    contributor = getUserInfo(project.UserID)
    if 'username' not in login_session:
        return render_template('publiconeproject.html', category=category,
                               project=project, photos=photos,
                               contributor=contributor)
    else:
        if login_session['user_id'] == project.UserID:
            return render_template('oneproject.html', category=category,
                                   project=project, photos=photos,
                                   contributor=contributor)
        else:
            return render_template('publiconeproject.html', category=category,
                                   project=project, photos=photos,
                                   contributor=contributor)


# **************************************************************************
# ADD PROJECT:
# **************************************************************************
@app.route('/category/<int:category_id>/projects/new', methods=['GET', 'POST'])
def newProject(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(
        CategoryID=category_id).one()
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        if request.files.get("picture") is not None:
            file = request.files.get("picture")
            filename = file.filename
            destination = "/".join([target, filename])
            file.save(destination)
            newProject = Project(
                ProjectName=request.form['name'],
                ProjectDesc=request.form['description'],
                CategoryID=category_id,
                DateAdd=datetime.now().replace(microsecond=0),
                DateEdit=datetime.now().replace(microsecond=0),
                ProjectLocation=request.form['location'],
                ProjectPicture=filename,
                UserID=login_session['user_id'])
        else:
            newProject = Project(
                ProjectName=request.form['name'],
                ProjectDesc=request.form['description'],
                CategoryID=category_id,
                DateAdd=datetime.now().replace(microsecond=0),
                DateEdit=datetime.now().replace(microsecond=0),
                ProjectLocation=request.form['location'],
                ProjectPicture='default.jpg',
                UserID=login_session['user_id'])
        session.add(newProject)
        session.commit()

        if request.files.get("additional-pictures") is not None:
            for file2 in request.files.getlist("additional-pictures"):
                filename2 = file2.filename
                destination = "/".join([target, filename2])
                file2.save(destination)
                newPicture = UploadFile(
                    FileName=filename2, ProjectID=newProject.ProjectID)
                session.add(newPicture)
                session.commit()
        flash("New Project Created!")
        return redirect(url_for('showProjects', category_id=category_id))
    else:
        return render_template('newproject.html', category_id=category_id, category=category)


# **************************************************************************
# EDIT PROJECT
# **************************************************************************
@app.route('/category/<int:category_id>/projects/<project_id>/edit',
           methods=['GET', 'POST'])
def editProject(category_id, project_id):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedProject = session.query(Project).filter_by(
        ProjectID=project_id).one()
    editedPhotos = session.query(UploadFile).filter_by(
        ProjectID=project_id).all()
    if editedProject.UserID != login_session['user_id']:
        output = ""
        output += "<script>function myFunction() {alert('You are not "
        output += "authorized to edit this Project. Please access one of "
        output += "the projects you created or create a new project "
        output += "in order to edit.'); window.location.href = '/';}"
        output += "</script><body onload='myFunction()''>"
        return output
    if request.method == 'POST':
        if request.form['name']:
            editedProject.ProjectName = request.form['name']
            editedProject.ProjectDesc = request.form['description']
            editedProject.ProjectLocation = request.form['location']
            editedProject.DateEdit = datetime.now().replace(microsecond=0)
            target = os.path.join(APP_ROOT, 'static/images/')
            if not os.path.isdir(target):
                os.mkdir(target)
            if request.files.get("picture") is not None:
                file = request.files.get("picture")
                filename = file.filename
                destination = "/".join([target, filename])
                file.save(destination)
                editedProject.ProjectPicture = filename
            else:
                if editedProject.ProjectPicture is None:
                    editedProject.ProjectPicture = 'default.jpg'

            if request.files.get("additional-pictures") is not None:
                for file2 in request.files.getlist("additional-pictures"):
                    filename2 = file2.filename
                    additionalPicture = session.query(UploadFile).filter_by(
                        ProjectID=project_id).filter_by(
                        FileName=filename2).first()
                    if additionalPicture is None:
                        destination = "/".join([target,
                                                filename2])
                        file2.save(destination)
                        newPicture = UploadFile(
                            FileName=filename2, ProjectID=project_id)
                        session.add(newPicture)
                        session.commit()
        session.add(editedProject)
        session.commit()
        flash("Project Successfully Edited!")
        return redirect(url_for('showOneProject', category_id=category_id,
                                project_id=project_id))
    else:
        return render_template('editproject.html', category_id=category_id,
                               project_id=project_id, project=editedProject)


# **************************************************************************
# DELETE PROJECT:
# **************************************************************************
@app.route('/category/<int:category_id>/projects/<project_id>/delete',
           methods=['GET', 'POST'])
def deleteProject(category_id, project_id):
    if 'username' not in login_session:
        return redirect('/login')
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    deletedProject = session.query(
        Project).filter_by(ProjectID=project_id).one()
    if deletedProject.UserID != login_session['user_id']:
        output = ""
        output += "<script>function myFunction() {alert('You are not "
        output += "authorized to delete this Project. Please access one of "
        output += "the projects you created or create a new project "
        output += "in order to delete.'); window.location.href = '/';}"
        output += "</script><body onload='myFunction()''>"
        return output
    if request.method == 'POST':
        projectPictures = session.query(
            UploadFile).filter_by(ProjectID=project_id).all()
        if projectPictures is not None:
            for picture in projectPictures:
                deletedPicture = session.query(
                    UploadFile).filter_by(FileID=picture.FileID).one()
                session.delete(deletedPicture)
                session.commit()

        session.delete(deletedProject)
        session.commit()

        flash("Project Successfully Deleted!")
        return redirect(url_for('showProjects', category_id=category_id))
    else:
        return render_template('deleteproject.html', category_id=category_id,
                               project_id=project_id, project=deletedProject)


# **************************************************************************
# JSON API Endpoints:
# **************************************************************************

# JSON Endpoint to view Category data
# **************************************************************************
@app.route('/category/<int:category_id>/projects/JSON')
def categoryProjectsJSON(category_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(
        CategoryID=category_id).one()
    projects = session.query(Project).filter_by(
        CategoryID=category.CategoryID)
    return jsonify(Projects=[p.serialize for p in projects])


# JSON Endpoint to view Individual Project data
# **************************************************************************
@app.route('/category/<int:category_id>/projects/<int:project_id>/JSON')
def projectJSON(category_id, project_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    project = session.query(Project).filter_by(
        ProjectID=project_id).one()
    return jsonify(Project=project.serialize)


# JSON Endpoint to view Category/Project data
# **************************************************************************
@app.route('/category/JSON')
def categoriesJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
