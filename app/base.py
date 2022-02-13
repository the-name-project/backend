from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class Service(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, session: Session, *, object_data: CreateSchemaType) -> ModelType:
        model_object = self.model.from_orm(object_data)
        session.add(model_object)
        session.commit()
        session.refresh(model_object)
        return model_object

    def find_all(
        self, session: Session, *, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        statement = select(self.model).offset(offset).limit(limit)
        return session.exec(statement).all()

    def find_one(self, session: Session, id: Any) -> Optional[ModelType]:
        return session.get(self.model, id)

    def update(
        self,
        session: Session,
        *,
        model_object: ModelType,
        object_data: UpdateSchemaType,
    ) -> ModelType:
        update_data = object_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(model_object, key, value)
        session.add(model_object)
        session.commit()
        session.refresh(model_object)
        return model_object

    def remove(self, session: Session, *, model_object: ModelType) -> None:
        session.delete(model_object)
        session.commit()
