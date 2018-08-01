from app import db
import datetime as dt
class Mixin(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update_dict(self, dic):
        for key, value in dic.items():
            if key == "date": value = self.date_factory(value)
            setattr(self, key, value)

    def date_factory(self, d):
        if isinstance(d, str):
            return dt.datetime.strptime(d, "%Y-%m-%d")
        else:
            return d

class User(Mixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.String(24), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(8), nullable=False)
    minutes = db.Column(db.Integer)
    disabled = db.Column(db.Boolean, default=False)

    def __init__(self, data = None):
        self.auth_id = data.get("auth_id", "")
        self.name = data.get("name", "")
        self.phone = data.get("phone", "")
        self.minutes = data.get("minutes", 0)
    def __repr__(self):
        return '<User %r>' % (self.name)

class Day(Mixin,db.Model):
    __tablename__ = 'days'

    date = db.Column(db.Date, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    minutes = db.Column(db.Integer, default=0)
    weekend = db.Column(db.Boolean)

    def __init__(self, data=None):
        date = data.get("date", "")
        self.date = self.date_factory(date)
        self.uid = data.get("uid", "")
        self.weekend = data.get("weekend", False)

    def __repr__(self):
        return '<Day %r>' % (str(self.date))

class Weekend(Mixin,db.Model):
    __tablename__ = 'weekends'

    date = db.Column(db.Date, primary_key=True)
    weekend = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, data=None):
        date = data.get("date", "")
        self.date = self.date_factory(date)
        self.weekend = data.get("weekend", False)

    def __repr__(self):
        return '<Weekend %r>' % (str(self.date))

class Holiday(Mixin,db.Model):
    __tablename__ = 'holidays'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    uid = db.Column(db.Integer, nullable=False)

    def __init__(self, data=None):
        date = data.get("date", "")
        self.date = self.date_factory(date)
        self.uid = data.get("uid", "")

    def __repr__(self):
        return '<Holiday %r>' % (str(self.date))