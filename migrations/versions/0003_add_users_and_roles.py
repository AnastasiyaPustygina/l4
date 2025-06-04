"""Add initial roles and users"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision = '0003_add_users_and_roles'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_unique_constraint('uq_role_name', 'role', ['name'])

    op.execute("""
        INSERT INTO role (name)
        VALUES ('admin'), ('user')
        ON CONFLICT (name) DO NOTHING;
    """)

    op.execute("""
        INSERT INTO users (username, password_hash, first_name, last_name, middle_name, role_id, is_active, created_at)
        VALUES 
        (
            'admin',
            'scrypt:32768:8:1$uMWs5G39oT92Vbom$9d84748016322e7712432765e64f97eb4fe08536a339dd21abf4112d01e035d4060bb98d15cf008e408b4f80b74993a260d51286600ccd1c957366b8d185662a',
            'Admin',
            'Adminov',
            'Adminovich',
            (SELECT id FROM role WHERE name = 'admin' LIMIT 1),
            TRUE,
            NOW()
        ),
        (
            'user1',
            'scrypt:32768:8:1$uMWs5G39oT92Vbom$9d84748016322e7712432765e64f97eb4fe08536a339dd21abf4112d01e035d4060bb98d15cf008e408b4f80b74993a260d51286600ccd1c957366b8d185662a',
            'User',
            'Userov',
            'Userovich',
            (SELECT id FROM role WHERE name = 'user' LIMIT 1),
            TRUE,
            NOW()
        ),
        (
            'user2',
            'scrypt:32768:8:1$uMWs5G39oT92Vbom$9d84748016322e7712432765e64f97eb4fe08536a339dd21abf4112d01e035d4060bb98d15cf008e408b4f80b74993a260d51286600ccd1c957366b8d185662a',
            'User',
            'Petrov',
            'Ivanovich',
            (SELECT id FROM role WHERE name = 'user' LIMIT 1),
            TRUE,
            NOW()
        ),
        (
            'user3',
            'scrypt:32768:8:1$uMWs5G39oT92Vbom$9d84748016322e7712432765e64f97eb4fe08536a339dd21abf4112d01e035d4060bb98d15cf008e408b4f80b74993a260d51286600ccd1c957366b8d185662a',
            'User',
            'Sidorov',
            'Petrovich',
            (SELECT id FROM role WHERE name = 'user' LIMIT 1),
            TRUE,
            NOW()
        ),
        (
            'myTestUser',
            'scrypt:32768:8:1$uMWs5G39oT92Vbom$9d84748016322e7712432765e64f97eb4fe08536a339dd21abf4112d01e035d4060bb98d15cf008e408b4f80b74993a260d51286600ccd1c957366b8d185662a',
            'myTestUser',
            'surnameTest',
            'testchectvo',
            (SELECT id FROM role WHERE name = 'admin' LIMIT 1),
            TRUE,
            NOW()
        ), (
            'user4',
            'scrypt:32768:8:1$uMWs5G39oT92Vbom$9d84748016322e7712432765e64f97eb4fe08536a339dd21abf4112d01e035d4060bb98d15cf008e408b4f80b74993a260d51286600ccd1c957366b8d185662a',
            'User',
            'Kuznetsov',
            'Alexandrovich',
            (SELECT id FROM role WHERE name = 'user' LIMIT 1),
            TRUE,
            NOW()
        );
    """)

def downgrade():

    op.execute("""
        DELETE FROM users WHERE username IN ('admin', 'user1', 'user2', 'user3', 'user4');
    """)


    op.execute("""
        DELETE FROM role WHERE name IN ('admin', 'user');
    """)

    op.drop_constraint('uq_role_name', 'role', type_='unique')
