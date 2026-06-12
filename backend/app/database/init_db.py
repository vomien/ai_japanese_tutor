from app.database.base import Base
from app.database.database import engine

import app.models.user
import app.models.conversation
import app.models.message

Base.metadata.create_all(
    bind=engine
)

print("Database initialized")