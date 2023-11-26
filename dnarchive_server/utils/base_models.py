from typing import Any

from pydantic import BaseModel


class GCModel(BaseModel):
    content: str
    skew: str

class G4Model(BaseModel):
    id: int
    position: int
    length: int
    score: float
    sequence: str
    sub_score: str

class ChromosomeListModel(BaseModel):
    id: int
    length: int
    name: str
    ref_seq: str  # Ref Seq ID
    updated_at: str  # Last modification in database
    g4_count: int  # Number of Quadruplexes in chromosome

class StatsModel(BaseModel):
    g4_frequency: dict[float, float]  # Frequency of Quadruplex occurence for given threshold
    g4_threshold_count: dict[float, int]  # Count of Quadruplex occurence for given threshold
    gc: dict[GCModel, float]  # GC content for chromosome
    id: int
    length: int
    name: str
    ref_seq: str  # Ref Seq ID
    updated_at: str  # Last modification in database