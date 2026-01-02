# app/routers/tmdb.py
from fastapi import APIRouter, HTTPException, Query, Path
import httpx
from app.services.tmdb_client import TMDBClient

router = APIRouter(prefix="/uas/tmdb", tags=["UAS - TMDB"])

@router.get("/ping")
def ping_tmdb_router():
    return {"message": "UAS TMDB router connected"}

@router.get("/movies")
async def list_movies(
    page: int = Query(1, ge=1),
    language: str = Query("id-ID"),
):
    try:
        data = await TMDBClient().get_popular_movies(page=page, language=language)

        results = []
        for m in data.get("results", []):
            results.append({
                "id": m.get("id"),
                "title": m.get("title"),
                "overview": m.get("overview"),
                "release_date": m.get("release_date"),
                "vote_average": m.get("vote_average"),
                "poster_path": m.get("poster_path"),
            })

        return {
            "page": data.get("page"),
            "total_pages": data.get("total_pages"),
            "total_results": data.get("total_results"),
            "results": results
        }

    except httpx.HTTPStatusError as e:
        # forward status code dari TMDB (401, 404, dll)
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"TMDB upstream error: {str(e)}")


@router.get("/movies/{movie_id}")
async def movie_detail(
    movie_id: int = Path(..., ge=1),
    language: str = Query("id-ID"),
    append: str | None = Query(None, description="contoh: videos,credits"),
):
    try:
        m = await TMDBClient().get_movie_detail(
            movie_id=movie_id,
            language=language,
            append_to_response=append,
        )

        return {
            "id": m.get("id"),
            "title": m.get("title"),
            "tagline": m.get("tagline"),
            "overview": m.get("overview"),
            "release_date": m.get("release_date"),
            "runtime": m.get("runtime"),
            "vote_average": m.get("vote_average"),
            "genres": [g.get("name") for g in m.get("genres", [])],
            "poster_path": m.get("poster_path"),
        }

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"TMDB upstream error: {str(e)}")
