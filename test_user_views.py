

from app import app, CURR_USER_KEY
import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Follows, bcrypt
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, session, g

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app
# from seed import seed_data


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
    """Test for the Message model."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password='PASSWORD',
            image_url=None
        )

        db.session.add(u)
        db.session.commit()

        self.user = u

        u_two = User.signup(
            email="test2@test.com",
            username="testuserasDASKD",
            password='PASSWORD',
            image_url=None
        )
        u_two.id = 2
        db.session.add(u_two)
        db.session.commit()

        test_follow = Follows(user_being_followed_id=u.id,
                              user_following_id=u_two.id)
        db.session.add(test_follow)
        db.session.commit()

        test_follow_2 = Follows(user_being_followed_id=u_two.id,
                                user_following_id=u.id)
        db.session.add(test_follow_2)
        db.session.commit()

        test_message = Message(text='i am whiskey',
                               user_id=self.user.id, timestamp=datetime.utcnow())
        db.session.add(test_message)
        db.session.commit()

        self.message = test_message

    def test_view_following(self):
        """Test to see if you can see following pages when logged in."""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            resp = client.get(f'users/{self.user.id}/following')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="col-lg-4 col-md-6 col-12" id="following_cards">',
                          resp.data.decode('utf-8'))

    def test_logged_out_visiting(self):
        """Test to see if you are prevented from viewing a user's follower/following page if you are not logged in"""

        with app.test_client() as client:
            resp = client.get(
                f'users/{self.user.id}/following')
            html = resp.get_data(as_text=True)
            # import pdb; pdb.set_trace()
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/")

    def test_adding_a_message(self):
        """Testing to see if logged in user can send a message as themselves"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            resp = client.post('/messages/new')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            user = User.query.get_or_404(self.user.id)
            msg_len = len(user.messages)
            user_message = Message(text='i am whiskey',
                                   user_id=user.id, timestamp=datetime.utcnow())
            db.session.add(user_message)
            db.session.commit()
            self.assertEqual(len(user.messages), msg_len + 1)

    def test_deleting_a_message(self):
        """Testing to see if logged in user can delete a message as themselves"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            user = User.query.get_or_404(self.user.id)
            msg = Message.query.get_or_404(user.messages[0].id)
            msg_len = len(user.messages)
            resp = client.post(f'messages/{msg.id}/delete')
            self.assertEqual(resp.status_code, 302)
            db.session.delete(msg)
            db.session.commit()
            self.assertEqual(len(user.messages), msg_len - 1)

    