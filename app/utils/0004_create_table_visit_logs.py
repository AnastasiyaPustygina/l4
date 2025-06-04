from alembic import op
import sqlalchemy as sa

revision = '0004_create_table_visit_log'
down_revision = '0003_add_users_and_roles'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'visit_log',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('path', sa.String(length=100)),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('visit_log')