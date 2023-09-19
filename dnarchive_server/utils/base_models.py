from typing import Any

from pydantic import BaseModel

class G4Model(BaseModel):
    id: int
    position: int
    length: int
    score: float
    sequence: str
    sub_score: str

class PalindromeModel(BaseModel):
    sequence: str
    spacer: str
    length: int
    spacer_length: int
    mismatch_count: int
    position: int


class AnalysisOut(BaseModel):
    g4_hunter: list[G4Model]
    palindrome_finder: list[PalindromeModel]