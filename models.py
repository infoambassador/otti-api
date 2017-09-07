from app import db

# Use base class from SQLAlchemy
class Institution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    courses = db.relationship('Course', backref='institution', lazy='dynamic')
    sheet_name = db.Column(db.String(64), index=True, unique=False)

    def __repr__(self):
        return '<Inst %r>' % self.name

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    number = db.Column(db.String(64), index=True, unique=True)
    rubric = db.Column(db.String(64), index=True, unique=False)
    institution_id = db.Column(db.Integer, db.ForeignKey('institution.id'))


    def __repr__(self):
        return '<Crs %r>' % self.name
