from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(80),primary_key=True)
    password = db.Column(db.String(80),nullable=False)
    phoneNo=db.Column(db.String(15),nullable=False)
    userSubmissions = db.relationship("SubmissionStore", backref="user", lazy=True)

    def __init__(self, username, password,phoneNo):
        self.username = username
        self.password=password
        self.phoneNo = phoneNo

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_phoneNo(cls,phoneNo):
        return cls.query.filter_by(phoneNo=phoneNo).first()





class SubmissionStore(db.Model):
    __tablename__ = 'submission'

    id = db.Column(db.Integer, primary_key=True)
    title1 = db.Column(db.String(80))
    imageurl=db.Column(db.String(200))
    estimation=db.Column(db.String(50))
    user_id=db.Column(db.String(50),db.ForeignKey('users.username'))

    def __init__(self,title,imageurl,weight,user):
        self.title1=title
        self.imageurl=imageurl
        self.estimation=weight
        self.user_id=user

    def json(self):
        return { 'title': self.title1, 'imageurl': self.imageurl, 'estimation':self.estimation }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(user_id=username)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()
