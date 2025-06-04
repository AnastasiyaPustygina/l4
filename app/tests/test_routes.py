import unittest
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        user = User(
            username='myTestUser',
            first_name='Test',
            last_name='User',
            password_hash=generate_password_hash('pass'),
            is_active=True
        )
        db.session.add(user)
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        response = self.client.post('/auth/login', data={
            'login': 'myTestUser',
            'password': 'pass'
        }, follow_redirects=True)
        print(response.data.decode('utf-8'))  # Для отладки
        return response

    def test_homepage_after_login(self):
        self.login()
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Список пользователей', html)

    def test_homepage_redirects_to_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login', response.headers['Location'])

    def test_login_page(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('Вход', html)

if __name__ == '__main__':
    unittest.main()
