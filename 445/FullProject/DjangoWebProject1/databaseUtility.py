import sqlite3
from collections import namedtuple
from django.conf import settings



def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def getConnection():
    return sqlite3.connect(settings.DATABASES['default']['NAME'])
    #return sqlite3.connect("C:\Workspace\project\database\mydb.db")

def getCursor(db):
    return db.cursor()

def fetchOne(selectStatement):
    db = getConnection()
    cur = getCursor(db)
    cur.execute(selectStatement)

    return cur.fetchone()

def fetchAll(selectStatement):
    db = getConnection()
    cur = getCursor(db)
    cur.execute(selectStatement)
    
    return namedtuplefetchall(cur)
    #return cur.fetchall()

def executeStatement(statement):
    try:
        db = getConnection()
        cur = getCursor(db)
        cur.execute("PRAGMA foreign_keys = on")
        cur.execute(statement)
        db.commit()
        return True
    except :
        db.rollback()
        return False

def executeStatements(statements):
    try:
        db = getConnection()
        cur = getCursor(db)
        cur.execute("PRAGMA foreign_keys = on")
        for statement in statements:
            cur.execute(statement)        
        db.commit()
        return True
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        #exc_type, exc_value, exc_tb = sys.exc_info()
        #print(traceback.format_exception(exc_type, exc_value, exc_tb))
    except :
        db.rollback()
        return False
