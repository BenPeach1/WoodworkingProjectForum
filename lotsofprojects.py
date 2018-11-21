import datetime
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Project, User, UploadFile

# engine = create_engine('sqlite:///woodworking_projects.db')
engine = create_engine(
    'postgresql://catalog:Udcatalog2018!@localhost/woodworking_projects')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# ******************************************************************************
# INSERT USERS
# ******************************************************************************
# First User - Ben Peach
picture = "https://qph.fs.quoracdn.net/main-thumb-277675678-200-"
picture += "jyvnerbrmjihqalwpvclyaivxqfcgeat.jpeg"
user1 = User(Username="Al Borland",
             UserEmail="al@tooltime.com",
             UserPicture=picture)

session.add(user1)
session.commit()

# Second User - John Doe
picture = "https://vignette.wikia.nocookie.net/homeimprovement/images/1/11/"
picture += "Tim_Taylor.jpg/revision/latest?cb=20110519130703"
user2 = User(Username="Tim Taylor",
             UserEmail="tim@tooltime.com",
             UserPicture=picture)

session.add(user2)
session.commit()

# ***************************************************************************
# INSERT CATEGORIES & PROJECTS
# ***************************************************************************
# Projects for Woodturning***************************************************
category1 = Category(CategoryName="Woodturning",
                     CategoryDesc="Turning various wooden items on the lathe!",
                     CategoryPicture="cat_woodturning.jpg",
                     User=user1)

session.add(category1)
session.commit()

description = "Hard Maple and Purpleheart cup for holding pens and pencils."
dateAdd1 = datetime(2018, 10, 3, 10, 10, 10)
project1 = Project(ProjectName="Pencil Holder",
                   ProjectDesc=description,
                   DateAdd=dateAdd1,
                   DateEdit=dateAdd1,
                   Category=category1,
                   User=user1,
                   ProjectPicture="Pencil_Holder.jpg",
                   ProjectLocation="Detroit, MI")

session.add(project1)
session.commit()

# Projects for CNC***********************************************************
category2 = Category(CategoryName="CNC",
                     CategoryDesc="Projects created using a CNC router/laser!",
                     CategoryPicture="cat_CNC.jpg",
                     User=user1)

session.add(category2)
session.commit()

description = "Red Oak and Walnut hand-shaped surfboard engraved with "
description += "custom logo."
dateAdd2 = datetime(2018, 10, 3, 10, 10, 10)
project2 = Project(ProjectName="Engraved Surfboard",
                   ProjectDesc=description,
                   DateAdd=dateAdd2,
                   DateEdit=dateAdd2,
                   Category=category2,
                   User=user1,
                   ProjectPicture="Surf_BoardV2.jpg",
                   ProjectLocation="Detroit, MI")

session.add(project2)
session.commit()

description = "Bubinga tray designed to hold two stacks of Post-It notes."
dateAdd3 = datetime(2018, 10, 3, 10, 14, 14)
project3 = Project(ProjectName="Post-It Note Holder",
                   ProjectDesc=description,
                   DateAdd=dateAdd3,
                   DateEdit=dateAdd3,
                   Category=category2,
                   User=user2,
                   ProjectPicture="Post-it_Holder.jpg",
                   ProjectLocation="Columbus, OH")

session.add(project3)
session.commit()

# Projects for Home Improvement**********************************************
category3 = Category(CategoryName="Furniture",
                     CategoryDesc="Woodworking around the house!",
                     CategoryPicture="cat_Furniture.jpg",
                     User=user1)

session.add(category3)
session.commit()

description = "Built-in entertainment center with complete with flanking "
description += "bookshelves, component storage, and drawers."
dateAdd4 = datetime(2018, 10, 3, 10, 19, 10)
project4 = Project(ProjectName="Entertainment Center",
                   ProjectDesc=description,
                   DateAdd=dateAdd4,
                   DateEdit=dateAdd4,
                   Category=category3,
                   User=user1,
                   ProjectPicture="Entertainment_Center.jpg",
                   ProjectLocation="Detroit, MI")

session.add(project4)
session.commit()

extraPicture4_1 = UploadFile(
    Project=project4, FileName="EntCenter_1.jpg")
session.add(extraPicture4_1)
session.commit()

extraPicture4_2 = UploadFile(
    Project=project4, FileName="EntCenter_2.jpg")
session.add(extraPicture4_2)
session.commit()

extraPicture4_3 = UploadFile(
    Project=project4, FileName="EntCenter_3.jpg")
session.add(extraPicture4_3)
session.commit()

extraPicture4_4 = UploadFile(
    Project=project4, FileName="EntCenter_4.jpg")
session.add(extraPicture4_4)
session.commit()

extraPicture4_5 = UploadFile(
    Project=project4, FileName="EntCenter_5.jpg")
session.add(extraPicture4_5)
session.commit()

extraPicture4_6 = UploadFile(
    Project=project4, FileName="EntCenter_6.jpg")
session.add(extraPicture4_6)
session.commit()

extraPicture4_7 = UploadFile(
    Project=project4, FileName="EntCenter_7.jpg")
session.add(extraPicture4_7)
session.commit()

desecription = "Custom-built walk-in closet for the master bedroom."
dateAdd5 = datetime(2018, 10, 3, 10, 21, 10)
project5 = Project(ProjectName="Walk-in Closet",
                   ProjectDesc=description,
                   DateAdd=dateAdd5,
                   DateEdit=dateAdd5,
                   Category=category3,
                   User=user2,
                   ProjectPicture="Walk-in_Closet.jpg",
                   ProjectLocation="Columbus, OH")

session.add(project5)
session.commit()


# Projects for Drinkware*****************************************************
category4 = Category(CategoryName="Drinkware",
                     CategoryDesc="Projects to elevate your drink experience!",
                     CategoryPicture="cat_Drinkware.jpg",
                     User=user1)

session.add(category4)
session.commit()

description = "Walnut drink coasters engraved with custom epoxy-filled "
description += "Colorado logo."
dateAdd6 = datetime(2018, 10, 3, 10, 24, 10)
project6 = Project(ProjectName="Colorado Coasters",
                   ProjectDesc=description,
                   DateAdd=dateAdd6,
                   DateEdit=dateAdd6,
                   Category=category4,
                   User=user1,
                   ProjectPicture="Colorado_Coasters.jpg",
                   ProjectLocation="Detroit, MI")

session.add(project6)
session.commit()

dateAdd7 = datetime(2018, 10, 3, 10, 28, 10)
project7 = Project(ProjectName="Handheld Bottle Opener",
                   ProjectDesc="Handheld bottle opener made from Hard Maple.",
                   DateAdd=dateAdd7,
                   DateEdit=dateAdd7,
                   Category=category4,
                   User=user2,
                   ProjectPicture="Handheld_Bottle_Opener.jpg",
                   ProjectLocation="Columbus, OH")

session.add(project7)
session.commit()

description = "Wooden beer caddy to carry six beer bottles engraved with "
description += "custom logo."
dateAdd8 = datetime(2018, 10, 3, 10, 33, 10)
project8 = Project(ProjectName="Beer Caddy",
                   ProjectDesc=description,
                   DateAdd=dateAdd8,
                   DateEdit=dateAdd8,
                   Category=category4,
                   User=user1,
                   ProjectPicture="Beer_Caddy.jpg",
                   ProjectLocation="Detroit, MI")

session.add(project8)
session.commit()

extraPicture8_1 = UploadFile(
    Project=project8, FileName="Beer_Caddy_2.jpg")
session.add(extraPicture8_1)
session.commit()

extraPicture8_2 = UploadFile(
    Project=project8, FileName="Beer_Caddy_3.jpg")
session.add(extraPicture8_2)
session.commit()

description = "Wooden bottle opener with recessed magnets to for mounting "
description += "to metal surfaces and catching bottle caps."
dateAdd9 = datetime(2018, 10, 3, 10, 42, 10)
project9 = Project(ProjectName="Magnetic Bottle Opener",
                   ProjectDesc=description,
                   DateAdd=dateAdd9,
                   DateEdit=dateAdd9,
                   Category=category4,
                   User=user2,
                   ProjectPicture="Mag_Bottle_Opener.jpg",
                   ProjectLocation="Columbus, OH")

session.add(project9)
session.commit()

# Projects for Kitchen*******************************************************
category5 = Category(CategoryName="Kitchen",
                     CategoryDesc="Wooden projects for the kitchen!",
                     CategoryPicture="cat_Kitchen.jpg",
                     User=user1)

session.add(category5)
session.commit()

description = "Cutting Board made from Walnut, Cherry, and Purpleheard, "
description += "engraved with custom monogram."
dateAdd10 = datetime(2018, 10, 3, 10, 55, 10)
project10 = Project(ProjectName="Monogram Cutting Board",
                    ProjectDesc=description,
                    DateAdd=dateAdd10,
                    DateEdit=dateAdd10,
                    Category=category5,
                    User=user1,
                    ProjectPicture="CuttingBoard1.jpg",
                    ProjectLocation="Detroit, MI")

session.add(project10)
session.commit()

description = "In-drawer end grain knife block made from Maple and Walnut."
dateAdd11 = datetime(2018, 10, 3, 11, 5, 10)
project11 = Project(ProjectName="Knife Block",
                    ProjectDesc=description,
                    DateAdd=dateAdd11,
                    DateEdit=dateAdd11,
                    Category=category5,
                    User=user2,
                    ProjectPicture="Knife_Block.jpg",
                    ProjectLocation="Columbus, OH")

session.add(project11)
session.commit()

description = "Wooden cookbook stand made from Walnut, Cherry, and "
description += "Purpleheart, used for hands-free use of cookbooks in "
description += "the kitchen."
dateAdd12 = datetime(2018, 10, 3, 11, 13, 10)
project12 = Project(ProjectName="Cookbook Stand",
                    ProjectDesc=description,
                    DateAdd=dateAdd12,
                    DateEdit=dateAdd12,
                    Category=category5,
                    User=user1,
                    ProjectPicture="Cookbook_stand.jpg",
                    ProjectLocation="Detroit, MI")

session.add(project12)
session.commit()

# Projects for Outdoors******************************************************
category6 = Category(CategoryName="Outdoor",
                     CategoryDesc="Projects intended for outdoor use!",
                     CategoryPicture="cat_Outdoors.jpg",
                     User=user1)

session.add(category6)
session.commit()

description = "Beach table with cup holders and engraved with custom "
description += "palm tree logo."
dateAdd13 = datetime(2018, 10, 3, 11, 16, 10)
project13 = Project(ProjectName="Tropical Beach Table",
                    ProjectDesc=description,
                    DateAdd=dateAdd13,
                    DateEdit=dateAdd13,
                    Category=category6,
                    User=user1,
                    ProjectPicture="Tropical_Beach_Table.jpg",
                    ProjectLocation="Detroit, MI")

session.add(project13)
session.commit()

description = "Beach table with cup holders and engraved with a "
description += "police-themed Blue Line flag."
dateAdd14 = datetime(2018, 10, 3, 11, 21, 10)
project14 = Project(ProjectName="Blue Line Beach Table",
                    ProjectDesc=description,
                    DateAdd=dateAdd14,
                    DateEdit=dateAdd14,
                    Category=category6,
                    User=user2,
                    ProjectPicture="BlueLine_BeachTable.jpg",
                    ProjectLocation="Columbus, OH")

session.add(project14)
session.commit()

print "Projects Added!"
