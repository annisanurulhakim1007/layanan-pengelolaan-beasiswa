# app/services/tmdb_client.py
import httpx
from app.config import settings

class TMDBClient:
    def __init__(self) -> None:
        self.base_url = settings.TMDB_BASE_URL.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {settings.TMDB_BEARER_TOKEN}",
            "accept": "application/json",
        }

    async def get_popular_movies(self, page: int = 1, language: str = "en-US"):
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"{self.base_url}/movie/popular",
                headers=self.headers,
                params={"page": page, "language": language},
            )
            r.raise_for_status()
            return r.json()

    async def get_movie_detail(
        self,
        movie_id: int,
        language: str = "en-US",
        append_to_response: str | None = None,
    ):
        params = {"language": language}
        if append_to_response:
            params["append_to_response"] = append_to_response

        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"{self.base_url}/movie/{movie_id}",
                headers=self.headers,
                params=params,
            )
            r.raise_for_status()
            return r.json()
