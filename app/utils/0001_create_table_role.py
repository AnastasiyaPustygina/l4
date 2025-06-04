from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision = '0001_create_table_role'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Создаём таблицу role
    op.create_table(
        'role',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('description', sa.String(length=128))
    )

    op.execute(
        """
        INSERT INTO role (name, description) VALUES
        ('admin', 'Administrator role'),
        ('user', 'Regular user role')
        """
    )

def downgrade():
    # Удаляем таблицу role
    op.drop_table('role')



