from tenacity import retry, stop_after_attempt, wait_exponential
import requests

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_movie_data(url, title):
    response = requests.post(
        f"{url}/movie",
        json={"title": title},
        timeout=5  # seconds
    )
    response.raise_for_status()
    return response.json()
