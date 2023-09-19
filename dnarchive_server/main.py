from logging.config import dictConfig

from fastapi import FastAPI, Query

from conf.log_conf import log_config
from utils.enums import ChromosomeName, Analysis, Sorting
from utils.base_models import AnalysisOut
from utils.db_data import (
    get_sequence_from_mongo,
    get_g4_hunter,
    get_palindrome_finder,
    get_chromosomes,
)

dictConfig(log_config)
app = FastAPI()

@app.get("/")
async def root():
    return {
        "version": "v1",
        "status": "active",
        "message": "DNA Analyser T2T API. Explore our endpoints to get started. Visit docs for more information.",
        "endpoints": [
            { "url": "/sequence", "description": "Returns DNA sequence for given part of a chromosome." },
            { "url": "/analysis", "description": "Returns analysis data for given range in sequence (G4 Hunter, Palindrome Analyser)." },
            { "url": "/chromosomes", "description": "Returns all chromosome metadata." }
        ]
    }

@app.get("/sequence/")
async def get_sequence(chromosome: ChromosomeName = ChromosomeName.chr1, start: int = 0, end: int = 5000):
    """
    Returns sequence for given part of a chromosome with analysis data.
    """

    return {
        "sequence": get_sequence_from_mongo(chromosome, start, end),
        "analysis": {
            "g4_hunter": [g4 for g4 in get_g4_hunter(chromosome, start, end)],
            "palindrome_finder": [palindrome for palindrome in get_palindrome_finder(chromosome, start, end)],
        }
    }

@app.get("/analysis/", response_model=AnalysisOut)
async def get_analysis(
        type: list[Analysis] = Query([Analysis.all], alias="analysis"),
        chromosome: list[ChromosomeName] = Query([ChromosomeName.chr1]),
        start: int = Query(0),
        end: int = Query(5000),
        g4_threshold: float = Query(None, alias="g4-threshold"),
        g4_window: int = Query(None, alias="g4-window"),
        palindrome_size: str = Query(None, alias="palindrome-size"),
        palindrome_spacer: str = Query(None, alias="palindrome-spacer"),
        palindrome_mismatches: str = Query(None, alias="palindrome-mismatches"),
        sort_by: Sorting = Query(Sorting.position_asc),
    ):
    """
    Returns analysis data for given range in sequence (G4 Hunter, Palindrome Analyser) according to input filter.
    """
    g4_filter = {
        "position": {"$gte": start, "$lte": end+30},
    }
    if g4_threshold:
        g4_filter.update({"$or": [
            {"score": {"$lte": g4_threshold}},
            {"score": {"$gte": -g4_threshold}}
        ]})
    if g4_window:
        g4_filter.update({"length": {"$lte": g4_window}})


    palindrome_filter = {
        "position": {"$gte": start, "$lte": end+30},
    }
    if palindrome_size:
        size_low, size_high = map(int, palindrome_size.split("-"))
        palindrome_filter.update({"length": {"$gte": size_low, "$lte": size_high}})
    if palindrome_spacer:
        spacer_len_low, spacer_len_high = map(int, palindrome_spacer.split("-"))
        palindrome_filter.update({"spacer_length": {"$gte": spacer_len_low, "$lte": spacer_len_high}})
    if palindrome_spacer:
        mismatches = map(int, palindrome_mismatches.split(","))
        palindrome_filter.update({"mismatch_count": {"$in": mismatches}})


    return {
        "g4_hunter": get_g4_hunter(chromosome, start, end, g4_filter, sort_by) if type == Analysis.g4 or Analysis.all else [],
        "palindrome_finder": get_palindrome_finder(chromosome, start, end, palindrome_filter, sort_by) if type == Analysis.palindrome or Analysis.all else [],
    }


@app.get("/chromosomes/")
async def get_chromosome():
    """
    Returns chromosome metadata from database for all chromosomes.
    """

    return [chr for chr in get_chromosomes()]
