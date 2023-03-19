"""initial data

Revision ID: c869f3265127
Revises: 762aee7672c0
Create Date: 2023-03-15 00:07:06.337873

"""
import crud

from alembic import op
from sqlalchemy.orm import Session
from models import User
from core.config import settings
from core.security import get_password_hash
from dotenv import load_dotenv

load_dotenv()

# revision identifiers, used by Alembic.
revision = 'c869f3265127'
down_revision = '762aee7672c0'
branch_labels = None
depends_on = None


def upgrade():
    # Create a new database session
    bind = op.get_bind()
    db = Session(bind=bind)
    # Create initial data
    user = User(email=settings.FIRST_SUPERUSER_EMAIL,
                password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                is_superuser=True,
                )
    db.add(user)
    db.commit()


def downgrade() -> None:
    # Create a new database session
    bind = op.get_bind()
    db = Session(bind=bind)
    # Delete initial data
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    db.delete(user)
    db.commit()
