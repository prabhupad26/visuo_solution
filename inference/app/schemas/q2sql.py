from pydantic import BaseModel


class q2SQLRequest(BaseModel):
    question: str
    schema_info: str
    external_knowledge: str


class q2SQLResponse(BaseModel):
    sql_query: str
