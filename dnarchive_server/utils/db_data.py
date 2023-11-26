import logging

from utils.enums import ChromosomeName, Sorting
from utils.connections import get_mongodb


logger = logging.getLogger("dnarchive-logger")


def get_sequence_from_mongo(chromosome: list[ChromosomeName], start: int, end: int):
    
    dbname = get_mongodb()

    if chromosome:
        chromosome = chromosome[0]  # FIXME, mb return for all chromosomes
    collection_name = dbname[chromosome]
    logger.info("Getting DNA sequence from MongoDB [%s] %d - %d", chromosome, start, end)

    result = collection_name.find({"start": {"$gte": start}, "end": {"$lte": end+30}}, {"_id": 0})
    return [seq["seq"] for seq in result]


def get_g4_hunter(chromosomes: list[ChromosomeName], start: int, end: int, g4_filter: dict = {}, sort_by: str = Sorting.position_asc):
    
    dbname = get_mongodb()
    result = []

    for chr in chromosomes:
        collection_name = dbname[f"{chr}_g4"]
        logger.info("Getting G4 analysis from MongoDB [%s] %d - %d", chr, start, end+30)
        partial = collection_name.find(
            {"position": {"$gte": start, "$lte": end+30}, **g4_filter},
            {"_id": 0}
        )
        result += list(partial)


    sort_by_col, sort_by_dir = sort_by.value.split(",")
    sort_by_dir = True if sort_by_dir == "desc" else False

    if sort_by_col not in ["score", "postion"]:
        sort_by_col = "position"

    return sorted(result, key=lambda x: x[sort_by_col], reverse=sort_by_dir)

def get_chromosomes(meta_only: bool = False):

    dbname = get_mongodb()
    collection_name = dbname["stats"]

    if not meta_only:
        return collection_name.find({}, {"_id": 0})

    non_meta_columns = {"_id": 0, "g4_frequency": 0, "gc": 0}
    result = list(collection_name.find({}, non_meta_columns))
    for chromosome in result:
        chromosome["g4_count"] = sum(chromosome.pop("g4_threshold_count").values())
    return result
