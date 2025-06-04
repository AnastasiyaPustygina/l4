import unittest
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

class UserModelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(testing=True)
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        User.query.filter_by(username='testuser').delete()
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_create_user(self):
        user = User(username='testuser', password_hash=generate_password_hash('password123'))
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)

    def test_user_password_hash(self):
        user = User(username='testuser2', password_hash=generate_password_hash('password123'))
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.check_password('password123'))

if __name__ == '__main__':
    unittest.main()
