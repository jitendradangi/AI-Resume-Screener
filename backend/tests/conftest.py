import os
import sys
from pathlib import Path

# The app is imported as a package from the backend root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Tests never touch the database, but importing the app requires a URL.
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("ALGORITHM", "HS256")
