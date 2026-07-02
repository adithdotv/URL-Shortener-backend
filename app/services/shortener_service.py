from sqlalchemy.orm import Session

from app.models.url_model import URL
from app.utils.generator import generate_short_code

BASE_URL = "http://localhost:8000"


def _generate_unique_code(db: Session) -> str:
    while True:
        short_code = generate_short_code()
        exists = db.query(URL).filter(URL.short_code == short_code).first()
        if not exists:
            return short_code


def create_short_url(db: Session, url: str) -> URL:
    short_code = _generate_unique_code(db)

    db_url = URL(original_url=url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url


def get_url_by_code(db: Session, short_code: str) -> URL | None:
    return db.query(URL).filter(URL.short_code == short_code).first()


def build_short_url(short_code: str) -> str:
    return f"{BASE_URL}/{short_code}"
