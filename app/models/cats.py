from app import db

class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    color = db.Column(db.String)
    human_id= db.Column(db.Integer, db.ForeignKey('human.id'))
    human = db.relationship("Human", back_populates="cats")
    

# class Cat:
#     def __init__(self, id, name, color, personality):
#         self.id = id
#         self.name = name
#         self.color = color
#         self.personality = personality

