import unittest
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

class UserManagementTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(testing=True)
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        from app.models.role import Role
        from app.models.user import User

        admin_role = Role(name='admin')
        db.session.add(admin_role)
        db.session.commit()

        admin_user = User(username='admin', password_hash=generate_password_hash('adminpass'), role_id=admin_role.id)
        db.session.add(admin_user)
        db.session.commit()

        cls.admin_user = admin_user

        with cls.client:
            cls.client.post('/auth/login', data=dict(
                login='admin',
                password='adminpass'
            ), follow_redirects=True)
    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_create_user(self):
        response = self.client.post('/user/create', data=dict(
            username='newuser',
            password='NewPassword123',
            first_name='Alice',
            last_name='Wonderland',
            middle_name='Megan',
            role_id=1
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Список пользователей'.encode('utf-8'), response.data)


    def test_delete_user(self):
        user = User(username='user_to_delete', password_hash=generate_password_hash('password123'))
        db.session.add(user)
        db.session.commit()
        response = self.client.post(f'/user/{user.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(User, user.id))

if __name__ == '__main__':
    unittest.main()
