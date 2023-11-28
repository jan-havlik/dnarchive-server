import logging

from utils.enums import ChromosomeName, Sorting
from utils.connections import get_mongodb


logger = logging.getLogger("dnarchive-logger")


def get_sequence_from_mongo(chromosome: ChromosomeName, start: int, end: int):
    
    dbname = get_mongodb()

    collection_name = dbname[chromosome.value]
    logger.info("Getting DNA sequence from MongoDB [%s] %d - %d", chromosome, start, end)

    result = collection_name.find({"start": {"$gte": start}, "end": {"$lte": end}}, {"_id": 0, "start": 0, "end": 0})
    return "".join(x["seq"] for x in result)


def get_quadruplexes(chromosomes: list[ChromosomeName], start: int, end: int, threshold: float, g4_filter: dict = {}, sort_by: str = Sorting.position_asc):
    
    dbname = get_mongodb()

    threshold_base, threshold_decimal = str(threshold).split('.')

    results = []
    for chromosome in chromosomes:
        colname = f"analysis_{chromosome.value}_{threshold_base}_{threshold_decimal}"
        collection_name = dbname[colname]
        logger.info("Getting G4 analysis from MongoDB [%s] %d - %d", colname, start, end+30)
        
        partial = list(collection_name.find(
            {"position": {"$gte": start, "$lte": end+30}, **g4_filter},
            {"_id": 0}
        ))
        results += list(map(lambda x: {**x, "chromosome": chromosome.value, "threshold": threshold}, partial))

    sort_by_col, sort_by_dir = sort_by.value.split(",")
    sort_by_dir = True if sort_by_dir == "desc" else False

    if sort_by_col not in ["score", "position"]:
        sort_by_col = "position"

    return sorted(results, key=lambda x: x[sort_by_col], reverse=sort_by_dir)

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
