import logging

from enum import Enum

from utils.connections import get_mongodb


logger = logging.getLogger("dnarchive-logger")

class ChromosomeName(str, Enum):
    chr1 = "chr1"
    chr2 = "chr2"
    chr3 = "chr3"
    chr4 = "chr4"
    chr5 = "chr5"
    chr6 = "chr6"
    chr7 = "chr7"
    chr8 = "chr8"
    chr9 = "chr9"
    chr10 = "chr10"
    chr11 = "chr11"
    chr12 = "chr12"
    chr13 = "chr13"
    chr14 = "chr14"
    chr15 = "chr15"
    chr16 = "chr16"
    chr17 = "chr17"
    chr18 = "chr18"
    chr19 = "chr19"
    chr20 = "chr20"
    chr21 = "chr21"
    chr22 = "chr22"
    chrX = "chrX"
    chrY = "chrY"


def get_sequence_from_mongo(chromosome: ChromosomeName, start: int, end: int):
    
    dbname = get_mongodb()
    collection_name = dbname[chromosome]
    logger.info("Getting DNA sequence from MongoDB [%s] %d - %d", chromosome, start, end)

    result = collection_name.find({"start": {"$gte": start}, "end": {"$lte": end+30}}, {"_id": 0})
    return [seq["seq"] for seq in result]


def get_g4_hunter(chromosome: ChromosomeName, start: int, end: int):
    
    dbname = get_mongodb()
    collection_name = dbname[f"{chromosome}_g4"]
    logger.info("Getting G4 analysis from MongoDB [%s] %d - %d", chromosome, start, end+30)

    result = collection_name.find(
        {"position": {"$gte": start, "$lte": end+30}},
        {"_id": 0}
    )

    return result


def get_palindrome_finder(chromosome: ChromosomeName, start: int, end: int):
    
    dbname = get_mongodb()
    collection_name = dbname[f"{chromosome}_palindrome"]
    logger.info("Getting Palindrome analysis from MongoDB [%s] %d - %d", chromosome, start, end+30)

    result = collection_name.find(
        {"position": {"$gte": start, "$lte": end+30}},
        {"_id": 0}
    )

    return result


def get_chromosomes():

    dbname = get_mongodb()
    collection_name = dbname["meta"]

    return collection_name.find({}, {"_id": 0})
