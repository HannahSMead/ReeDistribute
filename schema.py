from sqlalchemy import (Column, ForeignKey, DateTime, Boolean, Integer, Float, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, select
from datetime import datetime
import db


"""
This is the database for the webapp ReeDistribute
All information collected by this program defaults to anonymous 

"""
Base = declarative_base() #Make it an OOP

class IdPrimaryKeyMixin(object):
    #An ID column we wish to add to all rows,
    #  it will be unique to the table and given incrementaly
    id = Column(Integer, primary_key=True, nullable = False)


class DateTimeMixin(object):
    #To Record the time each object was created and last updated
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now,
                        onupdate=datetime.now)


class Account(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    accounts is the table for the Account objects which hold the user information 
    """
    __tablename__='accounts' #Store all account objects in accounts

    # Columns:
    username = Column(String, nullable = False) #used for personalization
    password = Column(String, nullable = False) # used for authorization
    name = Column(String) #So the site can adress you by your chosen name
    email = Column(String, nullable = False) #Account's email for contacting
    account_token = Column(String) #Account's Stripe coustomer key
    admin = Column(Boolean, default = False) #If 0 then this account is not an admin


    def __repr__(self):
        ret = "<ID: %d, username: %s, email: %s, token: %s>" % (
                self.id, self.username, self.email, self.account_token)
        return ret

class Student(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    students is the table for LSES student users information, represented by the Student object
    """
    __tablename__ = 'students'
    
    # Columns:
    related_account = Column(Integer, nullable = False) #So we can easily locate the user information
    open_requests = Column(Integer, default=0) #The number of open requests by the student
    closed_requests = Column(Integer, default=0) #The number of requests which the student opened that are now closed (filled)
    gained_money = Column(Float, default=0) #The total amount of money this Student has gained
    approved = Column(Boolean, default = False) #There are certain actions an account is denied if unapproved


    def __repr__(self):
        ret = "<ID: %d, Opened Requests: %d, Closed Requests: %d, Money Gained: %d>" % (
                self.id, self.open_requests, self.closed_requests, self.gained_money)
        return ret


class Donor(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    donors is the table for people who wish to make donations, represented by Donor objects
    """
    __tablename__= 'donors'

    # Columns:
    related_account = Column(Integer, nullable = False) #So we can easily locate the user information
    donations_given = Column(Integer, default=0) #The number of requests this donor has gave to
    money_given = Column(Float, default=0) #The total amount of money this donor has donated

    def __repr__(self):
        ret = "<ID: %d, donations_given: %d, money_given: %d>" % (
                self.id, self.donations_given, self.money_given)
        return ret

class Request(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    requests is the table which holds all the requests represented by Request objects
    """
    __tablename__='requests'

    # Columns:
    requested_by = Column(Integer) #who gave the request
    amount_needed = Column(Float) #How much money do you need
    description = Column(String) #Why the user needs money or requests for physical goods
    amount_filled = Column(Float, default=0.0) #How much money has been raised
    anon = Column(Boolean, default=True) #Will the request be posted anonymously
    filled = Column(Boolean, default=False) #After the request is filled, it no longer needs to be donated to
    
    def __repr__(self):
        ret = "<ID: %d, Requested: %d, Filled: %d, Reason: %s>" % (
                self.id, self.amount_needed, self.amount_filled, self.description)
        return ret

    
class Donation(Base, IdPrimaryKeyMixin, DateTimeMixin):
    """
    donations is the table of Donation objects
    """
    __tablename__='donations'

    # Columns:
    to_request = Column(Integer, nullable = False) #which request is being filled
    from_donor = Column(Integer, nullable = False) #who is donating
    amount_given = Column(Float) #how much money is being donated
    charge_token = Column(String) #stripey?
    anon = Column(Boolean, default = True) #Send anonymously  

    def __repr__(self):
        ret = '<Donation Key: %d, donated: %f, from account: %s' % (
                self.id, self.amount_given, self.from_donor)
        return ret


#####################################################
def start_db():
    Base.metadata.create_all(db.engine)
