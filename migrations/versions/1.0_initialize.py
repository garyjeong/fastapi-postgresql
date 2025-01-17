"""initialize

Revision ID: 1.0
Revises: 
Create Date: 2024-12-25 16:45:07.451085

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1.0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("public.alembic_version")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "public.alembic_version",
        sa.Column(
            "version_num",
            sa.VARCHAR(length=32),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("version_num", name="alembic_version_pkey"),
    )
    # ### end Alembic commands ###
