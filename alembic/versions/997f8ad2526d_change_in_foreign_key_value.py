"""change in foreign key value

Revision ID: 997f8ad2526d
Revises: b5c45a0b647a
Create Date: 2024-01-23 17:52:46.116560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '997f8ad2526d'
down_revision: Union[str, None] = 'b5c45a0b647a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('author_detail', sa.Column('modified_at', sa.DateTime(), nullable=True))
    op.drop_column('author_detail', 'modify_at')
    op.add_column('book_information', sa.Column('modified_at', sa.DateTime(), nullable=True))
    op.drop_column('book_information', 'modify_at')
    op.add_column('book_review', sa.Column('modified_at', sa.DateTime(), nullable=True))
    op.drop_column('book_review', 'modify_at')
    op.add_column('user_information', sa.Column('modified_at', sa.DateTime(), nullable=True))
    op.drop_column('user_information', 'modify_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_information', sa.Column('modify_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('user_information', 'modified_at')
    op.add_column('book_review', sa.Column('modify_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('book_review', 'modified_at')
    op.add_column('book_information', sa.Column('modify_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('book_information', 'modified_at')
    op.add_column('author_detail', sa.Column('modify_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('author_detail', 'modified_at')
    # ### end Alembic commands ###
