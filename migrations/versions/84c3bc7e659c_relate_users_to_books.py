"""relate users to books

Revision ID: 84c3bc7e659c
Revises: d7c7c1d59333
Create Date: 2025-02-02 15:53:46.721945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '84c3bc7e659c'
down_revision: Union[str, None] = 'd7c7c1d59333'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('rating', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('review_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column('reviews', sa.Column('book_uid', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'reviews', 'books', ['book_uid'], ['uid'])
    op.drop_column('reviews', 'page_count')
    op.drop_column('reviews', 'language')
    op.drop_column('reviews', 'title')
    op.drop_column('reviews', 'author')
    op.drop_column('reviews', 'published_date')
    op.drop_column('reviews', 'publisher')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('publisher', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('reviews', sa.Column('published_date', sa.DATE(), autoincrement=False, nullable=False))
    op.add_column('reviews', sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('reviews', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('reviews', sa.Column('language', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('reviews', sa.Column('page_count', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'book_uid')
    op.drop_column('reviews', 'review_text')
    op.drop_column('reviews', 'rating')
    # ### end Alembic commands ###
