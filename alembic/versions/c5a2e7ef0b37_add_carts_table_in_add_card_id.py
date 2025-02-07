"""add carts table in add card_id

Revision ID: c5a2e7ef0b37
Revises: b873d1990ab1
Create Date: 2024-07-15 13:59:56.521913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5a2e7ef0b37'
down_revision: Union[str, None] = 'b873d1990ab1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('CartInfo', sa.Column('cart_id', sa.String(length=100), nullable=False))
    op.drop_constraint('CartInfo_user_id_fkey', 'CartInfo', type_='foreignkey')
    op.create_foreign_key(None, 'CartInfo', 'Carts', ['cart_id'], ['id'])
    op.drop_column('CartInfo', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('CartInfo', sa.Column('user_id', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'CartInfo', type_='foreignkey')
    op.create_foreign_key('CartInfo_user_id_fkey', 'CartInfo', 'UserInfo', ['user_id'], ['id'])
    op.drop_column('CartInfo', 'cart_id')
    # ### end Alembic commands ###
