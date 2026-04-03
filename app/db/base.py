from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models so Alembic can detect them
from app.models import user, project, project_member, task  # noqa: F401, E402