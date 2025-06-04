import unittest
from app import create_app, db
from app.models.user import User

class AuthenticationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        user = User(username='adminTest')
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        response = self.client.post('/auth/login', data=dict(
            login='adminTest',
            password='123456'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список пользователей'.encode('utf-8'), response.data)

    def test_logout(self):
        self.client.post('/auth/login', data=dict(
            login='adminTest',
            password='123456'
        ), follow_redirects=True)

        response = self.client.get('/auth/logout', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Вход'.encode('utf-8'), response.data)
