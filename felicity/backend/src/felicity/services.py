from typing import Any
from sqlalchemy.orm import Session


async def get_user_by_id(id: int, db: Session, model: object) -> Any:
    return db.query(model).filter(model.id == id).first()
