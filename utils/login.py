from hashlib import sha1
import sqlite3
from os import urandom

f = "data/chelve.db"
db = connect(f)
c = db.cursor()

def register(username, password):
    db = connect(f)
    c = db.cursor()
    try: #does table already exist?
        c.execute("SELECT * FROM USERS")
    except: #if not, this is the first user!
        c.execute("CREATE TABLE users (user TEXT, salt TEXT, password TEXT, events TEXT)")
    if reg == "": #if error message is blank then theres no problem, update database
        salt = urandom(10).encode('hex')
        print salt
        query = ("INSERT INTO users VALUES (?, ?, ?, '')")
        password = sha1(password + salt).hexdigest()
        c.execute(query, (user, salt, password))
        db.commit()
        db.close()
        return "You've succesfully registered!"
    db.commit()
    db.close()
    return reg#return error message

def login(username, password):
    db = connect(f)
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

def addEvent(username, eid):
    db = connect(f)
    c = db.cursor()
    query = ("SELECT events FROM users WHERE user=" + username)
    evts = c.execute(query)
    if eid in evts:
        return #if its already there it wont add it
    ####### basically replace that users events with evts + eid
