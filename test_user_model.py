"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app
# from seed import seed_data

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
        # seed_data()

        u_two = User(
            id=2,
            email="test2@test.com",
            username="testuserasDASKD",
            password="HASHED_PASSWORD"
        )
        db.session.add(u_two)
        db.session.commit()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            id=1,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr(self):
        """Testing the repr method."""

        self.assertEqual(User.__repr__(User(id=1, username='testuser',
                                            email='test@test.com')), "<User #1: testuser, test@test.com>")

    def test_is_following(self):
        """Testing if user1 is following user2."""
        
        test_query_one = User.query.get_or_404(1)
        test_query_two = User.query.get_or_404(2)
        test_follow = Follows(user_being_followed_id=test_query_one.id,
                              user_following_id=test_query_two.id)
        self.assertEqual(User.is_following(test_query_two, test_query_one), 1)
