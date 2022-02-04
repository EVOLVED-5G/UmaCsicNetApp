from datetime import datetime
from netapp import db


class Cell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cell_num = db.Column(db.String(128), index=True, unique=True)
    crop_type = db.Column(db.String(32), index=True)
    historics = db.relationship('Historic', backref='cell', lazy='dynamic')

    def __repr__(self):
        return '<Cell: {}, Type: {}>'.format(self.cell_num, self.crop_type)

class Historic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.String)
    humidity = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    crop = db.Column(db.String(32), index=True)
    cell_id = db.Column(db.Integer, db.ForeignKey('cell.id'))

    def __repr__(self):
        return '<Historic {}>'.format(self.timestamp)