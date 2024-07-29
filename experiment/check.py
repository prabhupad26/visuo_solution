import json

from tqdm import tqdm
from utils import is_query_runnable


def count_runnable_queries(jsonl_file):
    """
    Function to count the number of runnable queries from a JSONL file.
    """
    runnable_count = 0
    with open(jsonl_file, "r") as file:
        data_dict_list = json.load(file)
        for data_dict in tqdm(data_dict_list, desc="Processing data points..."):
            db_id = data_dict.get("db_id", "")
            if db_id:
                db_path = f"experiment/data/dev_databases/dev_databases/{db_id}/{db_id}.sqlite"
                query = data_dict.get("SQL", "")
                if query and is_query_runnable(db_path, query):
                    runnable_count += 1

    return runnable_count


# Path to the JSONL file
jsonl_file = "experiment/data/dev.json"

# Count runnable queries
runnable_queries_count = count_runnable_queries(jsonl_file)
print(f"Number of runnable queries: {runnable_queries_count}")
