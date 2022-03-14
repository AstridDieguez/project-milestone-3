from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comments', backref='user')
    def __init__(self, username):
        self.username = username
    def __repr__(self):
        rep = "<id: " + str(self.id) + ", username: " + str(self.username) + ">"
        return rep
    def is_active(self):
        return True
    def get_id(self):
        return self.id
    def is_authenticated(self):
        return self.authenticated
    def is_anonymous(self):
        return False
    
    def to_dict(self):
        dict = {}
        dict["id"] = self.id
        dict["username"] = self.username
        dict["authenticated"] = self.authenticated
        dict["comments"] = []
        
        for comment in self.comments:
            dict["comments"].append(comment.to_dict())

        return dict

    @classmethod
    def userExists(cls, user_name):
        search = cls.query.filter_by(username=user_name).first()
        print("search: " + str(search))
        print("Users: " + str(cls.query.all()))
        if not search:
            return False
        return True
    
    @classmethod
    def addUser(cls, username):
        user = cls(username)
        db.session.add(user)
        db.session.commit()
        print("Users: " + str(cls.query.all()))

    @classmethod
    def getUser(cls, username):
        user = cls.query.filter_by(username=username).first()
        return user

class Comments(db.Model):
    __tablename__ = "Comments"
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    movieID = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    def __init__(self, userID, movieID, comment, rating):
        self.userID = userID
        self.movieID = movieID
        self.comment = comment
        self.rating = rating
    def __repr__(self):
        rep = "<id: " + str(self.id) + ", userID: " + str(self.userID) + ", movieID: " + str(self.movieID) + ", comment: " + str(self.comment) +", rating: " + str(self.rating) + ">"
        return rep

    def to_dict(self):
        dict = {}
        dict["id"] = self.id
        dict["userID"] = self.userID
        dict["movieID"] = self.movieID
        dict["comment"] = self.comment
        dict["rating"] = self.rating
        dict["username"] = self.user.username
        return dict

    @classmethod
    def addComment(cls, userID, movieID, comment, rating):
        comment = cls(userID, movieID, comment, rating)
        db.session.add(comment)
        db.session.commit()

    @classmethod
    def deleteComment(cls, id):
        comment = cls.query.filter_by(id=id).first()
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return True
        return False  

    @classmethod
    def getMovieComments(cls, movieID):
        comments = cls.query.filter_by(movieID=movieID).all()
        return comments

    @classmethod
    def getMovieComments_list(cls, movieID):
        comments = cls.query.filter_by(movieID=movieID).all()
        c_list = []
        for comment in comments:
            c_list.append(comment.to_dict())
        return c_list

    @classmethod
    def deleteAllComments(cls):
        comments = cls.query.all()
        for comment in comments:
            db.session.delete(comment)
        db.session.commit()

    @classmethod
    def getComment(cls, userID, movieID):
        comment = cls.query.filter_by(userID=userID, movieID=movieID).first()
        return comment

    @classmethod
    def getAllComments(cls):
        comments = cls.query.all()
        return comments