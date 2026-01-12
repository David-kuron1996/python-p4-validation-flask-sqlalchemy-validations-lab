from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

# -----------------------
# AUTHOR MODEL
# -----------------------
class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    @validates('name')
    def validate_name(self, key, value):
        if not value or value.strip() == '':
            raise ValueError("Author name cannot be empty")

        value = value.strip()

        # Check for uniqueness
        existing_author = Author.query.filter_by(name=value).first()
        if existing_author and existing_author.id != getattr(self, 'id', None):
            raise ValueError(f"Author with name '{value}' already exists.")

        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value

# -----------------------
# POST MODEL
# -----------------------
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(250), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    # Allowed categories
    ALLOWED_CATEGORIES = ['Fiction', 'Non-Fiction']

    @validates('title')
    def validate_title(self, key, value):
        if not value or value.strip() == '':
            raise ValueError("Title cannot be empty")

        # Clickbait keywords
        clickbait_keywords = ['won\'t believe', 'secret', 'top', 'guess', 'reasons']
        lower_title = value.lower()
        if not any(keyword in lower_title for keyword in clickbait_keywords):
            raise ValueError("Title must be clickbait-y")

        return value.strip()

    @validates('content')
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError("Content must be at least 250 characters")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) > 250:
            raise ValueError("Summary cannot exceed 250 characters")
        return value

    @validates('category')
    def validate_category(self, key, value):
        if value not in self.ALLOWED_CATEGORIES:
            raise ValueError(f"Category must be one of: {self.ALLOWED_CATEGORIES}")
        return value
