from pydantic import BaseModel


class ResearchRequest(BaseModel):
    query: str
class ResearchResponse(BaseModel):
   query: str
   message: str
