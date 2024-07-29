import sqlite3
from typing import List, Optional

import pandas as pd
from data import DbInfo, SqlInfo, TableInfo
from tqdm import tqdm


def generate_sql_schema(table_infos, db_name) -> str:
    schema_parts = []

    for table_info in table_infos:
        if table_info.db.db_id == db_name:
            column_definitions = []
            for col_idx, col in enumerate(table_info.cols):
                # Determine column type based on the column description or name (simplified logic)
                col_type = "TEXT"
                col_descr = table_info.column_description[col_idx] if table_info.column_description else ""
                column_definitions.append(f"{col} {col_type} {col_descr}")

            # Add primary key definition
            if isinstance(table_info.primary_key, list) and len(table_info.primary_key) > 1:
                primary_keys = ", ".join([pk for pk in table_info.primary_key])
            else:
                primary_keys = table_info.primary_key
            column_definitions.append(f"PRIMARY KEY ({primary_keys})")

            # TODO: Foreign key missing

            # Create the CREATE TABLE statement
            table_schema = f"CREATE TABLE {table_info.table_name} ({', '.join(column_definitions)});"
            schema_parts.append(table_schema)

    return "\n".join(schema_parts)


def build_q2sql_model(q2info_json, table_infos):
    q2sql_infos = []
    for entry in tqdm(q2info_json, desc="Parsing query/questions json files..."):
        schema_str = generate_sql_schema(table_infos, entry["db_id"])
        sqlinfo = SqlInfo(
            question=entry["question"],
            query_gold=entry["SQL"],
            external_knowledge=entry["evidence"],
            schema_str=schema_str,
            difficulty=entry["difficulty"],
            db_id=entry["db_id"],
        )
        q2sql_infos.append(sqlinfo)

    return q2sql_infos


def create_models_from_json(table_info_json, db_info_path):
    db_infos = []
    table_infos = []

    for entry in tqdm(table_info_json, desc="Parsing table json files..."):
        db_info = DbInfo(db_id=entry["db_id"])
        db_infos.append(db_info)

        table_names = entry.pop("table_names")
        table_names_original = entry.pop("table_names_original")
        primary_keys_db = entry.pop("primary_keys")
        # column_names_db = entry.pop("column_names")
        column_names_db = entry.pop("column_names_original")
        foreign_keys_db = entry.pop("foreign_keys")

        for table_idx, table_name in enumerate(table_names):
            column_names = [col[1] for col in column_names_db if col[0] == table_idx]

            primary_keys = []
            for prima_col in primary_keys_db:
                if isinstance(prima_col, int):
                    if column_names_db[prima_col][0] == table_idx:
                        primary_keys.append(column_names_db[prima_col][1])
                else:
                    for col in prima_col:
                        if column_names_db[col][0] == table_idx:
                            primary_keys.append(column_names_db[col][1])

            foreign_keys = set()
            for foreign_key_ids in foreign_keys_db:
                for foreign_key in foreign_key_ids:
                    foreign_keys.add(column_names_db[foreign_key][1])

            db_descr_info_path = (
                f"{db_info_path}/{entry['db_id']}/database_description/{table_names_original[table_idx]}.csv"
            )
            column_descriptions, value_descriptions = get_cols_descr(db_descr_info_path, column_names)

            table_info = TableInfo(
                table_name=table_names_original[table_idx],
                cols=column_names,
                primary_key=primary_keys,
                foreign_key=list(foreign_keys),
                db=db_info,
                column_description=column_descriptions,
                value_descriptions=value_descriptions,
            )
            table_infos.append(table_info)

    return db_infos, table_infos


def get_cols_descr(csv_path, col_list):
    try:
        # Attempt to read the CSV file with UTF-8 encoding
        df = pd.read_csv(csv_path, encoding="utf-8")
    except UnicodeDecodeError:
        # If there is a UnicodeDecodeError, try reading with ISO-8859-1 encoding
        df = pd.read_csv(csv_path, encoding="ISO-8859-1")

    df = df.astype(str)
    df.fillna("", inplace=True)

    # Create a list of column descriptions in the order of the columns
    column_descriptions = df["column_description"].tolist()

    # Create a list of value descriptions in the order of the columns
    value_descriptions = df["value_description"].tolist()

    return column_descriptions, value_descriptions


def is_query_runnable(db_path, query):
    """
    Function to check if a query is runnable.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Execute the query
        cursor.execute(query)
        # Fetch one result to ensure it runs
        cursor.fetchone()
        # Close the connection
        conn.close()
        return True
    except Exception as e:
        # If there is any exception, the query is not runnable
        # print(f"Query failed: {query}\nError: {e}")
        return False


def execute_query(db_path, query):
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Execute the query
        cursor.execute(query)
        # Fetch one result to ensure it runs
        result = cursor.fetchone()
        # Close the connection
        conn.close()
        return result
    except Exception as e:
        # If there is any exception, the query is not runnable
        # print(f"Query failed: {query}\nError: {e}")
        return None
