import typer
import os
import json
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from summa.utils import fetch_movie_data

app = typer.Typer()
console = Console()

load_dotenv()

# ENV config
ENV = os.getenv("ENV", "local")
BASE_URL = (
    os.getenv("BACKEND_URL", "https://summa-backend.onrender.com")
    if ENV == "production"
    else "http://localhost:10000"
)

@app.command()
def fetch(
    title: str = typer.Option(..., "--title", "-t", help="Movie title to fetch"),
    save: bool = typer.Option(False, "--save", "-s", help="Save result to a local file"),
):
    """Fetch movie info from the backend"""

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Fetching movie info...", total=None)

        try:
            data = fetch_movie_data(BASE_URL, title)

            console.print(Panel.fit(f"[bold green]{data['title']}[/] ({data['year']})", title="🎬 Movie"))

            console.print(f"[cyan] Cast:[/] {data['cast']}")
            console.print(f"[magenta] Plot:[/] {data['plot']}")
            console.print(f"[yellow] Language:[/] {data.get('language', 'N/A')}")

            if save:
                filename = f"{title.lower().replace(' ', '_')}.json"
                with open(filename, "w") as f:
                    json.dump(data, f, indent=2)
                console.print(f"\n[green]Saved to[/] [bold]{filename}[/]")

        except Exception as e:
            console.print(f"[bold red] Error:[/] {e}")

def run():
    app()

if __name__ == "__main__":
    run()
