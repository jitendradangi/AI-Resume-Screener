from typing import Generic, TypeVar, Type

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
    ):
        self.model = model

    def create(
        self,
        db: Session,
        **kwargs,
    ) -> ModelType:
        obj = self.model(**kwargs)

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    def get_by_id(
        self,
        db: Session,
        obj_id: int,
    ) -> ModelType | None:
        return (
            db.query(self.model)
            .filter(self.model.id == obj_id)
            .first()
        )

    def get_by_public_id(
        self,
        db: Session,
        public_id: str,
    ) -> ModelType | None:
        return (
            db.query(self.model)
            .filter(self.model.public_id == public_id)
            .first()
        )

    def get_all(
        self,
        db: Session,
    ) -> list[ModelType]:
        return db.query(self.model).all()

    def update(
        self,
        db: Session,
        obj: ModelType,
        **kwargs,
    ) -> ModelType:
        for key, value in kwargs.items():
            setattr(obj, key, value)

        db.commit()
        db.refresh(obj)

        return obj

    def delete(
        self,
        db: Session,
        obj: ModelType,
    ) -> None:
        db.delete(obj)
        db.commit()