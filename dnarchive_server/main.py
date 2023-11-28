from logging.config import dictConfig

from fastapi import FastAPI, Query

from conf.log_conf import log_config
from utils.enums import ChromosomeName, Sorting
from utils.base_models import G4Model, ChromosomeListModel, StatsModel
from utils.db_data import (
    get_sequence_from_mongo,
    get_quadruplexes,
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
            { "url": "/chromosomes", "description": "Returns all chromosome metadata." },
            { "url": "/stats", "description": "Returns stats for all chromosomes in T2T." }
        ]
    }

@app.get("/sequence/")
async def get_sequence(chromosome: ChromosomeName = Query(ChromosomeName.chr1), start: int = 0, end: int = 50000):
    """
    Returns sequence for given part of a chromosome with analysis data.
    """

    return {
        "sequence": get_sequence_from_mongo(chromosome, start, end),
        "analysis": get_quadruplexes([chromosome], start, end, 1.2)
    }

@app.get("/analysis/", response_model=list[G4Model])
async def get_analysis(
        chromosome: list[ChromosomeName] = Query([ChromosomeName.chr1]),
        start: int = Query(0),
        end: int = Query(50000),
        g4_threshold: float = Query(1.2, alias="g4-threshold"),
        g4_window: int = Query(None, alias="g4-window"),
        sort_by: Sorting = Query(Sorting.position_asc),
    ):
    """
    Returns analysis data for given range in sequence (G4 Hunter, Palindrome Analyser) according to input filter.
    """
    g4_filter = {
        "position": {"$gte": start, "$lte": end+30},
    }
    if g4_window:
        g4_filter.update({"length": {"$lte": g4_window}})


    return get_quadruplexes(chromosome, start, end, g4_threshold, g4_filter, sort_by)


@app.get("/chromosomes/", response_model=ChromosomeListModel)
async def get_chromosome():
    """
    Returns chromosome metadata from database for all chromosomes.
    """

    return [chr for chr in get_chromosomes(meta_only=True)]

@app.get("/stats/", response_model=StatsModel)
async def get_stats():
    """
    Returns overall G4 stats for T2T genome.
    """

    return [chr for chr in get_chromosomes()]
