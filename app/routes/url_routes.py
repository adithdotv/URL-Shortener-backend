from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.url_schema import URLRequest, URLResponse
from app.services.shortener_service import (
    build_short_url,
    create_short_url,
    get_url_by_code,
)

router = APIRouter()


@router.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    db_url = create_short_url(db, request.url)

    return URLResponse(
        original_url=db_url.original_url,
        short_code=db_url.short_code,
        short_url=build_short_url(db_url.short_code),
    )


@router.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    db_url = get_url_by_code(db, short_code)

    if db_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=db_url.original_url)
