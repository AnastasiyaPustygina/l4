from alembic import op
import sqlalchemy as sa

revision = '0002_create_table_user'
down_revision = ('0001_create_table_role')
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=80), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(length=512)),
        sa.Column('first_name', sa.String(length=80)),
        sa.Column('last_name', sa.String(length=80)),
        sa.Column('middle_name', sa.String(length=80)),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('role.id')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('is_active', sa.BOOLEAN(), default=True)
    )


def downgrade():
    op.drop_table('users')