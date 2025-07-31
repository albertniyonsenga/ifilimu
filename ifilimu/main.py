import typer
import httpx
import sqlite3
from rich.console import Console
from rich.spinner import Spinner
from rich.table import Table
from rich import print
from pathlib import Path
from time import sleep
from functools import wraps
from .utils import fetch_summary, init_db, load_from_cache, save_to_cache


app = typer.Typer()
console = Console()

# Set base URLs
LOCAL_BACKEND = "http://127.0.0.1:8000"
PROD_BACKEND = "https://summa-api.onrender.com"
CACHE_DB = Path.home() / ".summa_cache.db"

# Retry decorator
def retry(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except httpx.RequestError:
                    sleep(delay)
                    continue
            raise Exception("Failed after retries.")
        return wrapper
    return decorator

# Setup SQLite cache
def init_db():
    with sqlite3.connect(CACHE_DB) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS cache (query TEXT PRIMARY KEY, result TEXT)"
        )

def save_to_cache(query: str, result: str):
    with sqlite3.connect(CACHE_DB) as conn:
        conn.execute("REPLACE INTO cache (query, result) VALUES (?, ?)", (query, result))

def load_from_cache(query: str):
    with sqlite3.connect(CACHE_DB) as conn:
        row = conn.execute("SELECT result FROM cache WHERE query=?", (query,)).fetchone()
        return row[0] if row else None

# Fetch from API
@retry()
def fetch_summary(text: str, backend_url: str):
    res = httpx.post(f"{backend_url}/summarize", json={"text": text}, timeout=10)
    res.raise_for_status()
    return res.json()["summary"]

@app.command()
def summarize(
    text: str = typer.Argument(..., help="Text to summarize"),
    prod: bool = typer.Option(False, "--prod", help="Use production backend"),
    save: bool = typer.Option(False, "--save", help="Save result to cache"),
):
    """
    Summarize a block of text using local or cloud AI backend.
    """
    init_db()

    backend = PROD_BACKEND if prod else LOCAL_BACKEND
    console.print(f"\n[bold cyan]Using backend:[/] {backend}\n")

    # Check offline cache
    cached = load_from_cache(text)
    if cached:
        console.print("[bold green]Loaded from cache:[/]")
        print(f"\nSummary:\n[bold yellow]{cached}[/]")
        return

    with console.status("[bold blue]Summarizing...", spinner="dots"):
        try:
            summary = fetch_summary(text, backend)
            if save:
                save_to_cache(text, summary)
            console.print("\n[bold green] Summary:[/]")
            print(f"[bold yellow]{summary}[/]")
        except Exception as e:
            console.print(f"[bold red] Error:[/] {str(e)}")
            typer.Exit(code=1)

if __name__ == "__main__":
    app()
