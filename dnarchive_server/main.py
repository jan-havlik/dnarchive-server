from logging.config import dictConfig

from fastapi import FastAPI

from conf.log_conf import log_config
from utils.db_data import (
    ChromosomeName,
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
        "message": "DNA Analyser T2T API. Explore our endpoints to get started.",
        "endpoints": [
            { "url": "/sequence", "description": "Returns DNA sequence for given part of a chromosome." },
            { "url": "/analysis", "description": "Returns analysis data for given range in sequence (G4 Hunter, Palindrome Analyser)." },
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

@app.get("/analysis/")
async def get_analysis(analysis: str = None, chromosome: ChromosomeName = ChromosomeName.chr1, start: int = 0, end: int = 5000):
    """
    Returns analysis data for given range in sequence (G4 Hunter, Palindrome Analyser) according to input filter.
    """

    return {
        "g4_hunter": [g4 for g4 in get_g4_hunter(chromosome, start, end)],
        "palindrome_finder": [palindrome for palindrome in get_palindrome_finder(chromosome, start, end)],
    }


@app.get("/chromosomes/")
async def get_chromosome():
    """
    Returns chromosome metadata from database for all chromosomes.
    """

    return [chr for chr in get_chromosomes()]
