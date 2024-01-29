"""Add new table

Revision ID: edcfa7e87f6c
Revises: 
Create Date: 2024-01-22 16:05:00.031855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'edcfa7e87f6c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_information',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('username', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modify_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('book_information',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title_name', sa.String(length=255), nullable=False),
    sa.Column('author_id', postgresql.UUID(), nullable=True),
    sa.Column('publication_year', sa.DateTime(), nullable=False),
    sa.Column('genre', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modify_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user_information.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('book_reviews',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('user_id', postgresql.UUID(), nullable=True),
    sa.Column('blog_id', postgresql.UUID(), nullable=True),
    sa.Column('rating', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modify_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['book_information.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_information.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_reviews')
    op.drop_table('book_information')
    op.drop_table('user_information')
    # ### end Alembic commands ###
