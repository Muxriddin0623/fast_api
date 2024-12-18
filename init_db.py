from database import *
from models import *

Base.metadata.create_all(bind=engine)
