from app.database.connection import engine
from app.database.base import Base

import app.models.user
import app.models.plugin

Base.metadata.create_all(bind=engine)

print("Database Created Successfully")