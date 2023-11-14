"""empty message

Revision ID: 43882cb6cc3b
Revises: 9a204103346c
Create Date: 2023-11-14 15:17:44.943844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43882cb6cc3b'
down_revision = '9a204103346c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.drop_column('purchased')

    with op.batch_alter_table('users_records', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'purchased',
                sa.BOOLEAN(),
                server_default=sa.text('false'), nullable=True
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_records', schema=None) as batch_op:
        batch_op.drop_column('purchased')

    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'purchased',
                sa.BOOLEAN(),
                server_default=sa.text('false'), nullable=True
            )
        )

    # ### end Alembic commands ###
