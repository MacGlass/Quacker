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
from app import app, CURR_USER_KEY
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
            # import pdb; pdb.set_trace()
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div class="col-lg-4 col-md-6 col-12">', html)
