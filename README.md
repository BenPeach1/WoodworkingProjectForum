# Project 2: Item Catelog (Woodworking Project Forum)
This web application demonstrates an item catalog functionality in the form of a woodworking project forum in which authorized users can add (post), edit, and delete their projects that they would like to share with the woodworking community. These woodworking projects are grouped into categories which can be added/edited/deleted by users with the appropriate access privileges (e.g., administrators/moderators). If a category contains projects posted by users, the application will not allow the category to be deleted.

# Prerequisites for Running the Application

### _Vagrant Virtual Machine_
This application runs on a Vagrant Virtual Machine. If you do not have Vagrant installed, [You can download it from vagrantup.com.](https://www.vagrantup.com/downloads) Install the version for your operating system.

### _Libraries_
You will need to install the following libraries to run this web application:
 - Flask (```$pip install flask```)
 - SQLAlchemy (```$pip install SQLAlchemy```)
 - SQLAlchemy - ImageAttach (```$pip install SQLAlchemy-ImageAttach```)

# Running the Woodworking Project Forum App
Once you have logged your terminal into the virtual machine (```$vagrant ssh```), change to the /vagrant/catalog directory by typing (```$cd /vagrant/catalog```). Type (```$ls```) to ensure that you are inside the directory that contains project.py, database_setup.py, and two directories named 'templates' and 'static'

##### _Database Setup_
Now type (```$python database_setup.py```) to initialize the database.

##### _Database Population_
Type (```$python lotsofprojects.py```) to populate the database with restaurants and menu items. (Optional)

##### _Run the Web Application_
Type (```$python project.py```) to run the Flask web server. In your browser visit **http://localhost:8000** to view the Woodworking Project Forum web app.
