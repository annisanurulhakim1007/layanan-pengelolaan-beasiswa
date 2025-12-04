from pydantic import BaseModel

class DecisionSchema(BaseModel):
    decision: str
