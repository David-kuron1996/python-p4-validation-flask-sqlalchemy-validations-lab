# seed.py
from random import choice as rc
from faker import Faker

from server import app
from models import db, Author, Post

fake = Faker()

with app.app_context():

    # Clear existing data
    Post.query.delete()
    Author.query.delete()
    db.session.commit()

    # Create authors
    authors = []
    for _ in range(25):
        author = Author(
            name=fake.unique.name(),  # ensure uniqueness
            phone_number=fake.unique.msisdn()[0:10]  # 10 digit phone
        )
        authors.append(author)
    db.session.add_all(authors)
    db.session.commit()

    # Clickbait titles for posts
    clickbait_titles = [
        "You Won't Believe What Happened!",
        "Top 10 Reasons This Works",
        "Secret Tricks to Save Money",
        "Guess What She Did Next!",
        "Reasons Why You Should Try This"
    ]

    # Create posts
    posts = []
    for _ in range(25):
        post = Post(
            title=rc(clickbait_titles),
            content='This is the content Secret ' * 50,  # 50*28=1400 chars > 250
            category=rc(['Fiction', 'Non-Fiction']),
            summary="This is a short summary",
            author_id=rc(authors).id
        )
        posts.append(post)

    db.session.add_all(posts)
    db.session.commit()

    print("Database seeded successfully!")
