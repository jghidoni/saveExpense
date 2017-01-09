'''
from app import db
from models import ExpenseRecord

db.create_all()

db.session.add(ExpenseRecord("ciao","mamma"))

db.session.commit()

'''
