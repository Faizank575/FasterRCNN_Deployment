# from db import db

# class SubmissionStore(db.Model):
#     __tablename__ = 'submission'


#     id = db.Column(db.Integer, primary_key=True)
#     title1 = db.Column(db.String(80))
#     # Imgur=db.Column(db.String(200))
#     estimation=db.Column(db.String(50))
#     user=db.Column(db.String(50),db.ForeignKey('users.username'))

#     def __init__(self,title,weight,user):
#         self.title1=title
#         self.estimation=weight
#         self.user=user

#     def json(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'items': [item.json() for item in self.items.all()]
#         }

#     @classmethod
#     def find_by_username(cls, username):
#         return cls.query.filter_by(username=username).first()

#     @classmethod
#     def find_all(cls):
#         return cls.query.all()

#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()
