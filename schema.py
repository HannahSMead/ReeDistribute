"""
This is the database for the webapp ReeDistribute
All information collected by this program remains anonymous
Everything that is stored is either for functionality or statistics to prove the site's valaccount_idity
TODO:
*connect up with the stripe goodies
*comments
*filled is now anon in requests
*no more account anon
*Question the validity of the __init__ methods
"""

from sqlalchemy import Column, ForeignKey, Boolean, Integer, Float, String, create_engine, select, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, reconstructor


Base = declarative_base() #Make an OOP
session = sessionmaker() #start the database session


class AccountMixin(object):
    """
    The mixin object for ReeDistribute Login.abs
    Attributes: account_id (int), name (str), email (str), consumer_key (str), admin (bool)
    These will be inheritied by both Student and Donor
    Mixin objects, like parent objects, enable classes to inherit traits
    """
    id = Column(Integer, primary_key=True) #The unique id for any account made on ReeDistribute
    username = Column(String, nullable = False) #Account's chosen name, used for site personalization
    email = Column(String, nullable = False) #Account's email for contacting
    consumer_key = Column(String) #Account's Stripe coustomer key
    admin = Column(Boolean) #If 0 then this account is not an admin
    def __init__(self, username, email, consumer_key, anon = True, admin = False):
        # Initialize account to the input values
        self.username = username
        self.email = email
        self.consumer_key = consumer_key 
        self.admin = admin

    def __repr__(self):
        # When called, accounts return the user's name
        return self.username

class Student(Base, AccountMixin):
    """
    The class for LSES students
    Attributes: account_id, open_requests (int), closed_requests (int), gained_money (int)
    """
    __tablename__ = 'students' #store all student Objects in students

    open_requests = Column(Integer) #The number of open requests by the student
    closed_requests = Column(Integer) #The number of requests which the student opened that are now closed (filled)
    gained_money = Column(Float) #The total amount of money this Student has gained (used for statistics)

    def __init__(self, username, email, consumer_key, admin = False):
        # Initializes the student with the account id and all other attributes set to 0
        self.open_requests = 0
        self.closed_requests = 0
        self.gained_money = 0
        self.username = username
        self.email = email
        self.consumer_key = consumer_key 
        self.admin = admin
    def __repr__(self):
        # Formats the student's information to be easily read
        s = "<ID: %d, Opened Requests: %d, Closed Requests: %d, Money Gained: %d>" % (self. account_id, self.open_requests, self.closed_requests, self.gained_money)
        return s

class Donor(Base, AccountMixin):
    """
    The class for Donors
    Attributes:  account_id (int), closed_requests (Int), money_given (int)
    """
    __tablename__= 'donors' #Store all donor objects in the table donors
    closed_requests = Column(Integer) #The number of requests this donor has closed (been the last one to donate to)
    money_given = Column(Float) #The total amount of money this donor has donated
    def __init__(self, username, email, consumer_key, anon = 1, admin = 0, closed_requests=0, money_given=0):
        # Initializes the donor with the account id and all other attributes set to 0
        self.closed_requests = closed_requests
        self.money_given = money_given
        self.username = username
        self.email = email
        self.consumer_key = consumer_key 
        self.anon = anon
        self.admin = admin
    def __repr__(self):
        #Formats the donor's information to be easily read
        ret = "<ID: %d, closed_requests: %d, money_given: %d>" % (self. account_id, self.closed_requests, self.money_given)
        return ret

class Request(Base):
    """
    The object class for donation requests
    Attributes: 
    """
    __tablename__='requests' #store all the request objects in a table called requests

    request_id = Column(Integer, primary_key=True, nullable = False)
    account_id = Column(Integer, primary_key = True, nullable = False)
    amount_needed = Column(Float)
    amount_filled = Column(Float)
    description = Column(String)
    filled = Column(Boolean)

    def __init__(self, request_id, account_id, amount_needed, description):
        self.request_id = request_id
        self.account_id = account_id
        self.amount_needed = amount_needed
        self.description = description
        self.amount_filled = 0
        self.filled = False
    def __repr__(self):
        s = "<Request ID: %d, Requested: %d, Filled: %d, Reason: %s>" % (self.request_id, self.amount_needed, self.amount_filled, self.description)
        return s

class Donation(Base):
    """
    The object class for donation donations
    Attributes: 
    """
    __tablename__='donations' #store all the request objects in a table called requests

    request_id = Column(Integer, primary_key=True, nullable = False)
    account_id = Column(Integer, primary_key = True, nullable = False)
    amount_given = Column(Float)
    charge_key = Column(String)
    filled = Column(Boolean)

    def __init__(self, request_id, account_id, amount_given, charge_key='', filled=False):
        self.request_id = request_id
        self.account_id = account_id
        self.amount_given = amount_given
        self.charge_key = charge_key
        self.filled = filled

    def __repr__(self):
        s = '<Donation Key: %s, donated: %f, from account: %s' % (self.request_id, self.amount_given, self.account_id)
        return s
################################################################################################################################################
#  The relavent functions below will eventually be moved to another file
#  The reason they are still here is to test both the schema and the queries themselves
#  They are not all currently functional

def Run():
    engine = create_engine('postgresql://postgres@localhost/accounts')
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)
    return session(), engine
Run()

def get_id():
    return 1
def new_student(username, email, anon, admin, s):
    stu = Student(username, email, 'key', anon, admin)
    s.add(stu)
    s.commit()
    s.close()
    return s, stu
def new_donor(username, email, anon, admin, s):
    don = Donor(username, email, 'key', anon, admin)
    s.add(don)
    s.commit()
    return s, don
def new_request(account_id, amount_needed, description, s):
    request_id = get_id()
    req = Request(request_id, account_id, amount_needed, description)
    s.add(req)
    s.commit()
    s.close()
    return s, req

def example_select(s):
    s, don = new_donor('Gerald', 'Banana@stuff.com', True, False, s)
    s.add(don)
    find_donor = select([Donor]).where(Donor.username=='Gerald')
    dothing = s.execute(find_donor)
    dothing
    print(dothing)
    person = dothing.fetchone()
    print(person.id)
    print(person.email)
    print(person.money_given)

    return s
def example_update(s):
    _, don = new_donor('Gerald', 'Banana@stuff.com', True, False, s)
    s.add(don)
    find_donor = select([Donor, Donor.money_given]).where(Donor.username=='Gerald')
    dothing = s.execute(find_donor).fetchone()
    # don = dothing.fetchone()
    # d = dothing.fetchone()
    # d = s.dothing.execute()
    print(find_donor)
    print(dothing)
    dothing['money_given'] += 3.49
    print(dothing['money_given'])
    
    # print(don[money_given])
    
    # print(d)
    # print(d.id)
    # d.money_given = 5.000
    # print(d.money_given)

    
def donate(request_num, account_num, amount, s):
    # find_donor = Donor.get(account_num)
    find_donor = s.query(Donor).get(account_num)

    # find_donor = select([Donor]).where(Donor.id==account_num)
    find_request = select([Request]).where(Request.request_id==request_num)
    request_select = s.execute(find_request)
    donor_select = s.execute(find_donor)
    print(donor_select)
    request = request_select.fetchone()
    donor = donor_select.fetchone()
    # print(donor.money_given)
    give(donor, amount)
    # sofar = donor.money_given
    # sofar += amount
    # update_donor = update(Donor.__table__).where(donor.id == account_num).values(money_given = donor.money_given + amount)
    s.execute(update_donor)
    print(donor)
    # donation = Donation(request_num, account_num, amount)
    # s.add(donation)
    s.commit()
    print(sofar)
    return donation

def make_accounts(s):
    s, stu =new_student('violet','hey@violet.com', True, False, s)
    s.add(stu)
    s, don = new_donor('georgia', 'on_my_mind@stuff.com', True, False, s)
    s.add(don)
    s, req = new_request(1, 40, 'I NEED A TOAD TODAY', s)
    s.add(req)
    s.commit()
    return s

def test():
    s, engine = Run()    
    s = make_accounts(s)
    s.commit()
    # example_select(s)
    example_update(s)
    
    # donation = donate(1, 1, 40, s)
    s.commit()
    s.close()

# test()