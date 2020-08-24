class Users(db.Model):
    id = db.Column(db.Integer primary_key=True)
    name = db.Column(db.String(10))
    pwd = db.Column(db.String(30))
    # email = db.Column(db.String(30))
    