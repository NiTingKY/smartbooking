from extension import db


class Item(db.Model):
    __tablename__ = 'item'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dollar = db.Column(db.Float)
    plat = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    detail = db.Column(db.String(255))
    user_id = db.Column(db.String(255))
    source = db.Column(db.String(255))
    is_delete = db.Column(db.Integer)
    is_income = db.Column(db.Integer)

    @staticmethod
    def init_db(user_id):
        return "data"

    def to_dict(self):
        return {
            'uid': self.uid,
            'dollar': self.dollar,
            'plat': self.plat,
            'create_time': self.create_time.isoformat() if self.create_time else None, 
            'update_time': self.update_time.isoformat() if self.update_time else None,  # 转换为 ISO 8601 格式的字符串
            'detail': self.detail,
            'user_id': self.user_id,
            'source': self.source,
            'is_delete': self.is_delete,
            'is_income': self.is_income
        }
