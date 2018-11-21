from sqlalchemy import (Column,
                        ForeignKey,
                        Integer,
                        String,
                        DateTime,
                        LargeBinary)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
from datetime import datetime

Base = declarative_base()


class User(Base):
    """Registered user information stored in db"""
    __tablename__ = 'User'

    UserID = Column(Integer, primary_key=True)
    Username = Column(String(50), nullable=False)
    UserEmail = Column(String(100))
    UserPicture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'UserID': self.UserID,
            'Username': self.Username,
            'UserEmail': self.UserEmail,
        }


class Category(Base):
    """Category information stored in db"""
    __tablename__ = 'Category'

    CategoryID = Column(Integer, primary_key=True)
    CategoryName = Column(String(75), nullable=False)
    CategoryDesc = Column(String(250))
    CategoryPicture = Column(String(250))
    UserID = Column(Integer, ForeignKey('User.UserID'))
    User = relationship(User)
    Projects = relationship("Project", cascade="all, delete-orphan")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'CategoryID': self.CategoryID,
            'CategoryName': self.CategoryName,
            'CategoryDesc': self.CategoryDesc,
            'Creator': self.User.Username,
            'CategoryPicture': self.CategoryPicture,
        }


class Project(Base):
    """Project information stored in db"""
    __tablename__ = 'Project'

    ProjectID = Column(Integer, primary_key=True)
    ProjectName = Column(String(100), nullable=False)
    ProjectDesc = Column(String(500))
    ProjectPicture = Column(String(250))
    ProjectLocation = Column(String(100))
    DateAdd = Column(DateTime)
    DateEdit = Column(DateTime)
    CategoryID = Column(Integer, ForeignKey('Category.CategoryID'))
    Category = relationship(Category)
    UserID = Column(Integer, ForeignKey('User.UserID'))
    User = relationship(User)
    Pictures = relationship(
        "UploadFile", cascade="all, delete-orphan")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'ProjectID': self.ProjectID,
            'ProjectName': self.ProjectName,
            'ProjectDesc': self.ProjectDesc,
            'DateAdd': self.DateAdd,
            'DateEdit': self.DateEdit,
            'CategoryID': self.CategoryID,
            'ProjectLocation': self.ProjectLocation,
            'ProjectPicture': self.ProjectPicture,
            'Contributor': self.User.Username,
            'ContibutorPicture': self.User.UserPicture,
        }


class UploadFile(Base):
    """Uploaded Files - specifically project pictures, stored in db"""
    __tablename__ = 'UploadFile'

    FileID = Column(Integer, primary_key=True)
    FileName = Column(String(300))
    ProjectID = Column(Integer, ForeignKey('Project.ProjectID'))
    Project = relationship(Project)


# engine = create_engine('sqlite:///woodworking_projects.db')
engine = create_engine(
    'postgresql://catalog:Udcatalog2018!@localhost/woodworking_projects')
Base.metadata.create_all(engine)
