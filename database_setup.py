from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
from datetime import datetime

Base = declarative_base()


class UploadFile(Base):
    __tablename__ = 'UploadFile'

    FileID = Column(Integer, primary_key=True)
    FileName = Column(String(300))
    Data = Column(LargeBinary)


class User(Base):
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
    __tablename__ = 'Category'

    CategoryID = Column(Integer, primary_key=True)
    CategoryName = Column(String(75), nullable=False)
    CategoryDesc = Column(String(250))
    CategoryPicture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'CategoryID': self.CategoryID,
            'CategoryName': self.CategoryName,
            'CategoryDesc': self.CategoryDesc,
        }


class Project(Base):
    __tablename__ = 'Project'

    ProjectID = Column(Integer, primary_key=True)
    ProjectName = Column(String(100), nullable=False)
    ProjectDesc = Column(String(500))
    ProjectPicture = Column(String(250))
    DateAdd = Column(DateTime)
    DateEdit = Column(DateTime)
    CategoryID = Column(Integer, ForeignKey('Category.CategoryID'))
    Category = relationship(Category)
    UserID = Column(Integer, ForeignKey('User.UserID'))
    User = relationship(User)

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
            'UserID': self.UserID,
        }


engine = create_engine('sqlite:///woodworking_projects.db')
Base.metadata.create_all(engine)
