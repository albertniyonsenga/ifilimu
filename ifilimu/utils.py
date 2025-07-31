import httpx
import sqlite3
from pathlib import Path
from time import sleep
from functools import wraps

# Constants
CACHE_DB = Path.home() / ".summa_cache.db"

# Retry Decorator
def retry(max_retries=3, delay=1):
    """
    Retry decorator for retrying HTTP calls or transient errors.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i < max_retries - 1:
                        sleep(delay)
                    else:
                        raise e
        return wrapper
    return decorator

# API Caller
@retry()
def fetch_summary(text: str, backend_url: str):
    """
    Makes a POST request to the backend to get a summary.
    """
    response = httpx.post(f"{backend_url}/summarize", json={"text": text}, timeout=10)
    response.raise_for_status()
    return response.json()["summary"]

# SQLite Cache
def init_db():
    """
    Initialize SQLite cache if it doesn't exist.
    """
    with sqlite3.connect(CACHE_DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cache (
                query TEXT PRIMARY KEY,
                result TEXT
            )
        """)

def save_to_cache(query: str, result: str):
    """
    Save a summary to the local cache.
    """
    with sqlite3.connect(CACHE_DB) as conn:
        conn.execute("REPLACE INTO cache (query, result) VALUES (?, ?)", (query, result))

def load_from_cache(query: str):
    """
    Retrieve a summary from the local cache if it exists.
    """
    with sqlite3.connect(CACHE_DB) as conn:
        row = conn.execute("SELECT result FROM cache WHERE query = ?", (query,)).fetchone()
        return row[0] if row else None
