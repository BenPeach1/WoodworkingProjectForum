import datetime
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Project, User, UploadFile

engine = create_engine('sqlite:///woodworking_projects.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# ******************************************************************************
# INSERT USERS
# ******************************************************************************
# First User - Ben Peach
user1 = User(Username="Ben Peach",
             UserEmail="benjamin.j.peach@gmail.com")

session.add(user1)
session.commit()

# Second User - John Doe
user2 = User(Username="John Doe", UserEmail="john.doe@fake.com")

session.add(user2)
session.commit()

# ******************************************************************************
# INSERT CATEGORIES & PROJECTS
# ******************************************************************************
# Projects for Woodturning******************************************************
category1 = Category(CategoryName="Woodturning",
                     CategoryDesc="Turning various wooden items on the lathe!",
                     CategoryPicture="default.jpg")

session.add(category1)
session.commit()

dateAdd1 = datetime(2018, 10, 3, 10, 10, 10)
project1 = Project(ProjectName="Pencil Holder", ProjectDesc="Hard Maple and Purpleheart cup for holding pens and pencils.",
                   DateAdd=dateAdd1, DateEdit=dateAdd1, Category=category1, User=user1, ProjectPicture="default.jpg")

session.add(project1)
session.commit()

# Projects for CNC**************************************************************
category2 = Category(CategoryName="CNC",
                     CategoryDesc="Projects designed and executed using a CNC router or laser!",
                     CategoryPicture="default.jpg")

session.add(category2)
session.commit()

dateAdd2 = datetime(2018, 10, 3, 10, 10, 10)
project2 = Project(ProjectName="Engraved Surfboard", ProjectDesc="Red Oak and Walnut hand-shaped surfboard engraved with custom logo.",
                   DateAdd=dateAdd2, DateEdit=dateAdd2, Category=category2, User=user1, ProjectPicture="default.jpg")

session.add(project2)
session.commit()

dateAdd3 = datetime(2018, 10, 3, 10, 14, 14)
project3 = Project(ProjectName="Post-It Note Holder", ProjectDesc="Bubinga tray custom designed to hold two stacks of Post-It notes.",
                   DateAdd=dateAdd3, DateEdit=dateAdd3, Category=category2, User=user2, ProjectPicture="default.jpg")

session.add(project3)
session.commit()

# Projects for Home Improvement*************************************************
category3 = Category(CategoryName="Home Improvement",
                     CategoryDesc="Woodworking around the house!",
                     CategoryPicture="default.jpg")

session.add(category3)
session.commit()

dateAdd4 = datetime(2018, 10, 3, 10, 19, 10)
project4 = Project(ProjectName="Entertainment Center", ProjectDesc="Built-in entertainment center with complete with flanking bookshelves, component storage, and drawers.",
                   DateAdd=dateAdd4, DateEdit=dateAdd4, Category=category3, User=user1, ProjectPicture="default.jpg")

session.add(project4)
session.commit()

dateAdd5 = datetime(2018, 10, 3, 10, 21, 10)
project5 = Project(ProjectName="Walk-in Closet", ProjectDesc="Custom-built walk-in closet for the master bedroom.",
                   DateAdd=dateAdd5, DateEdit=dateAdd5, Category=category3, User=user2, ProjectPicture="default.jpg")

session.add(project5)
session.commit()

# Projects for Drinkware********************************************************
category4 = Category(CategoryName="Drinkware",
                     CategoryDesc="Projects designed to enhance your favorite beverage!",
                     CategoryPicture="default.jpg")

session.add(category4)
session.commit()

dateAdd6 = datetime(2018, 10, 3, 10, 24, 10)
project6 = Project(ProjectName="Colorado Coasters", ProjectDesc="Walnut drink coasters engraved with custom epoxy-filled Colorado logo.",
                   DateAdd=dateAdd6, DateEdit=dateAdd6, Category=category4, User=user1, ProjectPicture="default.jpg")

session.add(project6)
session.commit()

dateAdd7 = datetime(2018, 10, 3, 10, 28, 10)
project7 = Project(ProjectName="Handheld Bottle Opener", ProjectDesc="Handheld bottle opener made from Hard Maple.",
                   DateAdd=dateAdd7, DateEdit=dateAdd7, Category=category4, User=user1, ProjectPicture="default.jpg")

session.add(project7)
session.commit()

dateAdd8 = datetime(2018, 10, 3, 10, 33, 10)
project8 = Project(ProjectName="Beer Caddy", ProjectDesc="Wooden beer caddy to carry six beer bottles engraved with custom logo.",
                   DateAdd=dateAdd8, DateEdit=dateAdd8, Category=category4, User=user1, ProjectPicture="default.jpg")

session.add(project8)
session.commit()

dateAdd9 = datetime(2018, 10, 3, 10, 42, 10)
project9 = Project(ProjectName="Magnetic Bottle Opener", ProjectDesc="Wooden bottle opener with recessed magnets to for mounting to metal surfaces and catching bottle caps.",
                   DateAdd=dateAdd9, DateEdit=dateAdd9, Category=category4, User=user1, ProjectPicture="default.jpg")

session.add(project9)
session.commit()

# Projects for Kitchen**********************************************************
category5 = Category(CategoryName="Kitchen",
                     CategoryDesc="Wooden projects for the kitchen!",
                     CategoryPicture="default.jpg")

session.add(category5)
session.commit()

dateAdd10 = datetime(2018, 10, 3, 10, 55, 10)
project10 = Project(ProjectName="Monogrammed Cutting Board", ProjectDesc="Cutting Board made from Walnut, Cherry, and Purpleheard, engraved with custom monogram.",
                    DateAdd=dateAdd10, DateEdit=dateAdd10, Category=category5, User=user1, ProjectPicture="default.jpg")

session.add(project10)
session.commit()

dateAdd11 = datetime(2018, 10, 3, 11, 5, 10)
project11 = Project(ProjectName="Knife Block", ProjectDesc="In-drawer end grain knife block made from Maple and Walnut.",
                    DateAdd=dateAdd11, DateEdit=dateAdd11, Category=category5, User=user1, ProjectPicture="default.jpg")

session.add(project11)
session.commit()

dateAdd12 = datetime(2018, 10, 3, 11, 13, 10)
project12 = Project(ProjectName="Cookbook Stand", ProjectDesc="Wooden cookbook stand made from Walnut, Cherry, and Purpleheart, used for hands-free use of cookbooks in the kitchen.",
                    DateAdd=dateAdd12, DateEdit=dateAdd12, Category=category5, User=user1, ProjectPicture="default.jpg")

session.add(project12)
session.commit()

# Projects for Outdoors*********************************************************
category6 = Category(CategoryName="Outdoors",
                     CategoryDesc="Projects intended for outdoor use!",
                     CategoryPicture="default.jpg")

session.add(category6)
session.commit()

dateAdd13 = datetime(2018, 10, 3, 11, 16, 10)
project13 = Project(ProjectName="Tropical Beach Table", ProjectDesc="Beach table with cup holders and engraved with custom palm tree logo.",
                    DateAdd=dateAdd13, DateEdit=dateAdd13, Category=category6, User=user1, ProjectPicture="default.jpg")

session.add(project13)
session.commit()

dateAdd14 = datetime(2018, 10, 3, 11, 21, 10)
project14 = Project(ProjectName="Blue Line Beach Table", ProjectDesc="Beach table with cup holders and engraved with a police-themed Blue Line flag.",
                    DateAdd=dateAdd14, DateEdit=dateAdd14, Category=category6, User=user1, ProjectPicture="default.jpg")

session.add(project14)
session.commit()

print "Projects Added!"
