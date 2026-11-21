from pydantic import BaseModel, Field


class {{entity_pascal}}Base(BaseModel):
    id: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=150)


class {{entity_pascal}}Create({{entity_pascal}}Base):
    pass


class {{entity_pascal}}Update(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)


class {{entity_pascal}}Response({{entity_pascal}}Base):
    model_config = {"from_attributes": True}
