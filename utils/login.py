from hashlib import sha1
import sqlite3
from os import urandom

f = "data/schweak.db"
db = sqlite3.connect(f)
c = db.cursor()

def regReqs(user, password):      #error message generator
    if len(password) < 8 or len(password) > 32:
        return "Password must be 8-32 characters"
    if len(user) < 8 or len(user) > 32:
        return "Username must be 8-32 characters"
    if duplicate(user):          #checks if username already exists
        return "Username already exists"
    if " " in user or " " in password:
        return "Spaces not allowed in user or password"
    if user==password:
        return "Username and password must be different"
    return ""

def duplicate(user):#checks if username already exists
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query, (user,))
    retVal = False
    for record in sel:
        retVal = True
    db.commit()
    db.close()
    return retVal
  
def register(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    try: #does table already exist?
        c.execute("SELECT * FROM USERS")
    except: #if not, this is the first user!
        c.execute("CREATE TABLE users (user TEXT, salt TEXT, password TEXT, events TEXT)")
    reg = regReqs(username, password);
    if reg == "": #if error message is blank then theres no problem, update database
        salt = urandom(10).encode('hex')
        print salt
        query = ("INSERT INTO users VALUES (?, ?, ?, '')")
        password = sha1(password + salt).hexdigest()
        c.execute(query, (username, salt, password))
        db.commit()
        db.close()
        return "You've succesfully registered!"
    db.commit()
    db.close()
    return reg#return error message

def login(username, password):
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query,(user,));

    #records with this username
    #so should be at most one record (in theory)

    for record in sel:
        password = sha1(password+record[1]).hexdigest()##record[1] is the salt
        if (password==record[2]):
            return ""#no error message because it will be rerouted to mainpage
        else:
            return "User login has failed. Invalid password"#error message
    db.commit()
    db.close()
    return "Username does not exist"#error message

def getEvents(username):###returns a list of saved events for a specified user
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("SELECT events FROM users WHERE user=" + username)
    sel = c.execute(query)
    for row in sel:
        return row[0].split("-")

def addEvent(username, eId):###add event id to saved events for a specified user
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query, (username,))
    old = ""
    for row in sel:
        old = row
    if eId in old[3]:
        return #if its already there it wont add it
    new = (old[0], old[1], old[2], old[3] + eId + '-')
    query = ("DELETE FROM users WHERE user=?")
    c.execute(query,(username,))
    query = ("INSERT INTO users VALUES (?,?,?,?)")
    c.execute(query, new)
    db.commit()
    db.close()
    ####### basically replace that users events with events + eid



def remEvent(username, eId):###add event id to saved events for a specified user
    db = sqlite3.connect(f)
    c = db.cursor()
    query = ("SELECT * FROM users WHERE user=?")
    sel = c.execute(query, (username,))
    old = ""
    for row in sel:
        old = row
    new = (old[0], old[1], old[2], old[3].replace(eId + "-", ""))
    query = ("DELETE FROM users WHERE user=?")
    c.execute(query, (username,))
    query = ("INSERT INTO users VALUES(?,?,?,?)")
    c.execute(query, new)
    db.commit()
    db.close()
    ####### basically replace that users events with events + eid
    


