from testit import *
import db





def create_student(username, name, password, email):
    s = db.get_session()

    Acc =  Account(username = username, name = name, password=password, email = email)
    s.add(Acc)
    s.flush()

    Stu = Student(related_account=Acc.id)
    s.add(Stu)
    s.commit()
    s.close()


def create_donor(username, password, email):
    s = db.get_session()

    Acc =  Account(username = username, password=password, email = email)
    s.add(Acc)
    s.flush()

    Don = Donor(related_account=Acc.id)
    s.add(Don)
    s.commit()
    s.close()


def open_request(student_id, amount, reason):
    s = db.get_session()

    req = Request(requested_by=student_id, amount_needed=amount, description=reason)
    s.add(req)
    s.commit()
    s.close()   
 

def donate(request_id, donor_id, amount):

    s = db.get_session()
    D = s.query(Donor).get(donor_id)
    R = s.query(Request).get(request_id)

    D.money_given += amount
    D.donations_given += 1
    R.amount_filled += amount

    if R.amount_needed >= R.amount_filled:
        R.filled = True

    d = Donation(to_request=request_id, from_donor=donor_id,amount_given = amount)

    s.add(d)
    s.commit()
    s.close()

def authenticate(usernameAttempt, passwordAttempt):
    s = db.get_session()
    A = s.query(Account).filter(Account.username==usernameAttempt).first()
    if A is None: ret = False
    elif (A.password == passwordAttempt): ret = True
    else: ret = False
    s.close()
    return ret



######################################################################################## TESTS

def test_donation():
    createStudent('Georgia', 'Pe@ch3s','On@my.mind')
    createDonor('Mr.Money-Bags', 'Ka-CH1NG!','monopolywinner@funny.money')
    openRequest(1,34,'I need money for Rent')
    donate(1,1,35.0)

def test_tables():
    
    s = db.get_session()

    # Check Creation
    A = Account(username = 'JOE',password='ultimatej03',email = 'Joeyjoe@joesph.com',account_token = '555XTZ')
    S = Student()
    D = Donor()
    R = Request(requested_by = 4, amount_needed = 60.00, description = "I NEED A TOAD. TRUST ME.")
    DM = Donation(to_request= 3, from_donor= 4,amount_given=55.9,charge_token='kEYKey', filled=False)

    s.add(A)
    s.add(S)
    s.add(D)
    s.add(R)
    s.add(DM) 
    s.commit()

    print(A, A.__table__, A.id)
    print(S, S.__table__)
    print(D, D.__table__)
    print(R, R.__table__)
    print(DM, DM.__table__)

    s.close()

def test_authentication():
    A = Account(username = 'LonelyLady',name = 'Eleanor Rigby', password='ringoSTA**',email = 'doIbelong@here.where',account_token = 'MCKENZIE')
    s = db.get_session()
    s.add(A)
    s.commit()
    r1 = authenticate("LonelyLady", "ringoSTA**")
    r2 = authenticate("LonelyLaddie", "ringoSTA**")
    r3 = authenticate("LonelyLady", "YOKO")
    s.close()
    print(r1, r2, r3)
# test_authentication()
