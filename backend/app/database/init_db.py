from app.database.base import Base
from app.database.database import engine

import app.models.user
import app.models.conversation
import app.models.message
import app.models.user_profile
import app.models.learning_profile

Base.metadata.create_all(
    bind=engine
)

print("Database initialized")