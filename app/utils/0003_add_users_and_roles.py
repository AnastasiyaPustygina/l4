"""Add initial roles and users"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision = '0003_add_users_and_roles'
down_revision = '0002_create_table_user'
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
            'scrypt:32768:8:1$abcd1234$abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc1',
            'User',
            'Userov',
            'Userovich',
            (SELECT id FROM role WHERE name = 'user' LIMIT 1),
            TRUE,
            NOW()
        ),
        (
            'user2',
            'scrypt:32768:8:1$abcd1235$abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc2',
            'User',
            'Petrov',
            'Ivanovich',
            (SELECT id FROM role WHERE name = 'user' LIMIT 1),
            TRUE,
            NOW()
        ),
        (
            'user3',
            'scrypt:32768:8:1$abcd1236$abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc3',
            'User',
            'Sidorov',
            'Petrovich',
            (SELECT id FROM role WHERE name = 'user' LIMIT 1),
            TRUE,
            NOW()
        ),
        (
            'myTestUser',
            'scrypt:32768:8:1$d8ZRCFvoSEkiGYqx$520bc40fd07fb44a8c86c636924c89b66c312053ed002e5ff76fb8d4db6f4740cd5cc4921c2c54344d96174e3178015c13474254fb9048ea47faad0ee3060041',
            'myTestUser',
            'surnameTest',
            'testchectvo',
            (SELECT id FROM role WHERE name = 'admin' LIMIT 1),
            TRUE,
            NOW()
        ), (
            'user4',
            'scrypt:32768:8:1$abcd1237$abc123abc123abc123abc123abc123abc123abc123abc123abc123abc123abc4',
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
