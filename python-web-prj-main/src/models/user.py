from extension import db


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    account = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    mail = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.String(255), nullable=False)
    birth = db.Column(db.DateTime)
    valid = db.Column(db.Integer)
    photo_adr = db.Column(db.String(255))

    def to_dict(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'account': self.account,
            'password': self.password,
            'phone': self.phone,
            'mail': self.mail,
            'sex': self.sex,
            'birth': self.birth.isoformat() if self.birth else None,
            'valid': self.valid,
            'photo_adr': self.photo_adr
        }
