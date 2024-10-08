"""#1

Revision ID: 6549f34b1095
Revises: 
Create Date: 2024-09-23 19:35:10.574000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6549f34b1095'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('integracao', sa.Column('conta_contabil_contra_partida', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('integracao', 'conta_contabil_contra_partida')
    # ### end Alembic commands ###
