import unittest
from app import create_app, db, VisitLog
from app.models.user import User
from app.models.role import Role
from werkzeug.security import generate_password_hash
from bs4 import BeautifulSoup


class UserManagerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(testing=True)
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        existing_role = Role.query.filter_by(name='test_admin').first()
        if existing_role:
            db.session.delete(existing_role)
            db.session.commit()

        cls.test_role = Role(name='test_admin', description='Administrator role')
        db.session.add(cls.test_role)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        cls.app_context.pop()

    def setUp(self):
        self.role = Role.query.filter_by(name='test_admin').first()
        self.user = User(
            username='testsuser1',
            password_hash=generate_password_hash('password123'),
            first_name='John',
            last_name='Doe',
            middle_name='Smith',
            role_id=self.role.id,
            is_active=True
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        VisitLog.query.filter_by(user_id=self.user.id).delete()
        db.session.delete(self.user)
        db.session.commit()

    def login(self, username='testsuser1', password='password123'):
        return self.client.post('/auth/login', data={
            'login': username,
            'password': password
        }, follow_redirects=True)

    def extract_text(self, response):
        soup = BeautifulSoup(response.data, 'html.parser')
        return soup.get_text()

    def test_login_page(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Вход', self.extract_text(response))

    def test_login_user(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список', self.extract_text(response))

    def test_login_invalid_user(self):
        response = self.client.post('/auth/login', data={
            'login': 'testsuser1123',
            'password': 'wrongpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Пользователь не найден', self.extract_text(response))

    def test_login_invalid_password(self):
        response = self.client.post('/auth/login', data={
            'login': 'testsuser1',
            'password': 'wrongpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Неверный пароль', self.extract_text(response))

    def test_create_user(self):
        self.login()
        response = self.client.post('/user/create', data={
            'username': 'newuser',
            'password': 'NewPassword123',
            'first_name': 'Alice',
            'last_name': 'Wonderland',
            'middle_name': 'Megan',
            'role_id': self.role.id
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Создать пользователя', self.extract_text(response))
        self.assertIsNotNone(User.query.filter_by(username='newuser').first())

    def test_view_user(self):
        self.login()
        response = self.client.get(f'/user/{self.user.id}')
        self.assertEqual(response.status_code, 200)
        text = self.extract_text(response)
        self.assertIn('Фамилия', text)
        self.assertIn('John', text)
        self.assertIn('Doe', text)
        self.assertIn('Smith', text)

    def test_edit_user(self):
        self.login()
        response = self.client.post(f'/user/{self.user.id}/edit', data={
            'login': 'testsuser1',
            'password': 'NewPassword123',
            'first_name': 'John',
            'last_name': 'Doe',
            'middle_name': 'Smith',
            'role_id': self.role.id
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Главная', self.extract_text(response))
        updated_user = User.query.get(self.user.id)
        self.assertTrue(updated_user.check_password('NewPassword123'))

    def test_delete_user(self):
        self.login()
        user_to_delete = User(
            username='todelete',
            password_hash=generate_password_hash('password123'),
            first_name='To',
            last_name='Delete',
            middle_name='User',
            role_id=self.role.id
        )
        db.session.add(user_to_delete)
        db.session.commit()

        response = self.client.post(f'/user/{user_to_delete.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список пользователей', self.extract_text(response))
        self.assertIsNone(User.query.get(user_to_delete.id))

    def test_change_password(self):
        self.login()
        response = self.client.post('/auth/change-password', data={
            'old_password': 'password123',
            'new_password': 'NewPassword123',
            'confirm_password': 'NewPassword123'
        }, follow_redirects=True)

        self.assertIn('Пароль успешно изменён', self.extract_text(response))
        updated_user = User.query.get(self.user.id)
        self.assertTrue(updated_user.check_password('NewPassword123'))

    def test_logout(self):
        self.login()
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Вход', self.extract_text(response))


if __name__ == '__main__':
    unittest.main()
