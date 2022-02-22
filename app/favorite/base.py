from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)


class Service(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def find_all(
        self, session: Session, *, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        statement = select(self.model).offset(offset).limit(limit)
        return session.exec(statement).all()

    def find_one(self, session: Session, id: Any) -> Optional[ModelType]:
        return session.get(self.model, id)

