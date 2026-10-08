from pydantic import BaseModel

class TopicResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}

class SubjectResponse(BaseModel):
    id: int
    name: str
    description: str
    topics: list[TopicResponse] = []

    model_config = {"from_attributes": True}
