from datetime import datetime
from src import db

# Cell table in database
class Cell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cell_num = db.Column(db.String(120), index=True, unique=True)
    historics = db.relationship('Historic', backref='cell', lazy='dynamic')

# Historic table in database
class Historic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cell_id = db.Column(db.Integer, db.ForeignKey('cell.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    HS10_0 = db.Column(db.Float)
    HS10_1 = db.Column(db.Float)
    HS10_2 = db.Column(db.Float)
    HS30_0 = db.Column(db.Float)
    HS30_1 = db.Column(db.Float)
    HS30_2 = db.Column(db.Float)
    HS50_0 = db.Column(db.Float)
    HS50_1 = db.Column(db.Float)
    HS50_2 = db.Column(db.Float)
    FullBR = db.Column(db.Float)
    AirTC = db.Column(db.Float)
    RH = db.Column(db.Float)
