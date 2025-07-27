import typer
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Loading variables from .env

app = typer.Typer()

OMDB_API_KEY =os.getenv("OMDB_API_KEY")

def fetch_movie(title: str, year: str = None):
    params = {
        "t": title,
        "apikey": OMDB_API_KEY
    }
    if year:
        params["y"] = year

    try:
        response = requests.get("http://www.omdbapi.com/", params=params)
        print("Final Request URL:", response.url)  # Debug line
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            typer.secho(f"Error: {data.get('Error')}", fg=typer.colors.RED)
            raise typer.Exit()
        return data

    except requests.HTTPError as e:
        typer.secho(f"HTTP Error: {e}", fg=typer.colors.RED)
        typer.secho(f"Response content: {response.text}", fg=typer.colors.YELLOW)
        raise typer.Exit()
    except requests.RequestException as e:
        typer.secho(f"Network error: {e}", fg=typer.colors.RED)
        raise typer.Exit()


@app.command()
def movie(
    title: str = typer.Argument(..., help="Title of the movie"),
    year: str = typer.Option(None, "--year", "-y", help="Release year of the movie"),
    save: bool = typer.Option(False, "--save", "-s", help="Save the movie plot to a file")
):
    """
    Search for a movie and optionally save its plot.
    """
    if not OMDB_API_KEY:
        typer.secho("OMDB_API_KEY not found in environment.", fg=typer.colors.RED)
        raise typer.Exit()

    data = fetch_movie(title, year)
    typer.secho(f"\n🎬 {data['Title']} ({data['Year']})", fg=typer.colors.CYAN, bold=True)
    typer.echo(f"Genre: {data.get('Genre', 'N/A')}")
    typer.echo(f"IMDb: {data.get('imdbRating', 'N/A')}")
    typer.echo(f"\nPlot:\n{data['Plot']}")

    if save:
        filename = f"{data['Title'].replace(' ', '_')}_plot.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{data['Title']} ({data['Year']})\n\n{data['Plot']}")
        typer.secho(f"\nPlot saved to {filename}", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()

