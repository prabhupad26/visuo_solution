from typing import List, Union, Optional
from pydantic import BaseModel


class DbInfo(BaseModel):
    db_id: str


class TableInfo(BaseModel):
    table_name: str
    cols: List[str]
    primary_key: Union[str, List[str], None]
    foreign_key: Union[str, List[str], None]
    column_description: Optional[List[str]] = None
    value_description: Optional[List[str]] = None
    db: DbInfo

    def __init__(self, **data):
        super().__init__(**data)
        if self.column_description and len(self.column_description) != len(self.cols):
            raise ValueError("column_description must have the same length as cols")
        if self.value_description and len(self.value_description) != len(self.cols):
            raise ValueError("value_description must have the same length as cols")


class SqlInfo(BaseModel):
    question: str
    query_gold: str
    query_predicted: Optional[str] = None
    external_knowledge: Optional[str] = None
    difficulty: str
    schema_str: str
    db_id: str
