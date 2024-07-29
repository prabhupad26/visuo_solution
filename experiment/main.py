import json
import os
from tqdm import tqdm
import wandb
import pandas as pd
from utils import (
    create_models_from_json,
    build_q2sql_model,
    execute_query,
    is_query_runnable,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import yaml
import argparse


class q2SQLExperiment:
    def __init__(
        self,
        table_info_path,
        query2SQL_info_path,
        base_prompt_path,
        sys_prompt_path,
        db_info_path,
        model_params,
        difficulty=None,
        debug_num=None,
        api_key="<your_api_key>",
    ):
        self.table_info_path = table_info_path
        self.query2SQL_info_path = query2SQL_info_path
        self.base_prompt_path = base_prompt_path
        self.sys_prompt_path = sys_prompt_path
        self.db_info_path = db_info_path
        self.debug_num = int(debug_num) if debug_num else debug_num
        self.api_key = api_key
        self.table_infos = None
        self.q2sql_infos = None
        self.model = None
        self.base_prompt = None
        self.sys_prompt = None
        self.difficulty = difficulty
        self.sql_data = pd.DataFrame()
        self.tp = 0
        self.ls_tp = 0
        self.total_queries = 0
        self.init_wandb()
        self.load_data()
        self.initialize_model(**model_params)
        self.load_prompts()

    def init_wandb(self):
        wandb.init(project="visuo-challenge")

    def load_data(self):
        with open(self.table_info_path) as f:
            table_info_json = json.load(f)
        with open(self.query2SQL_info_path) as f:
            q2info_json = json.load(f)
        _, self.table_infos = create_models_from_json(
            table_info_json, self.db_info_path
        )
        self.q2sql_infos = build_q2sql_model(q2info_json, self.table_infos)

    def initialize_model(
        self, url, temperature, max_tokens=512, model_name="localhost"
    ):
        if model_name == "localhost":
            self.model = ChatOpenAI(
                temperature=temperature,
                openai_api_base=url,  # "http://localhost:8080/",
                openai_api_key=self.api_key,  # Dummy key
                max_tokens=max_tokens,
            )
        else:
            self.model = ChatOpenAI(
                temperature=temperature,
                base_url=url,  # "https://api.together.xyz/v1",
                api_key=self.api_key,
                model=model_name,
                max_tokens=max_tokens,
            )

    def load_prompts(self):
        with open(self.base_prompt_path, "r") as file:
            self.base_prompt = file.read()
        with open(self.sys_prompt_path, "r") as file:
            self.sys_prompt = file.read()

    def run_inference(self):
        if self.debug_num:
            self.q2sql_infos = self.q2sql_infos[: self.debug_num]
        if self.difficulty:
            self.q2sql_infos = [
                d for d in self.q2sql_infos if d.difficulty == self.difficulty
            ]
        for idx, query_info in tqdm(
            enumerate(self.q2sql_infos),
            desc="Running inference...",
            total=len(self.q2sql_infos),
        ):
            prompt_template = ChatPromptTemplate.from_messages(
                [("system", self.sys_prompt), ("user", self.base_prompt)]
            )
            parser = StrOutputParser()
            chain = prompt_template | self.model | parser
            response = chain.invoke(
                {
                    "schema_info": query_info.schema_str,
                    "external_knowledge": query_info.external_knowledge,
                    "question": query_info.question,
                }
            )

            db_path = (
                f"{self.db_info_path}/{query_info.db_id}/{query_info.db_id}.sqlite"
            )
            response = response.replace("\n", "")

            result = self.evaluate_response(response, query_info, db_path)
            self.log_results(idx, query_info, response, result)

    def evaluate_response(self, response, query_info, db_path):
        result = False
        if response.lower() == query_info.query_gold.lower():
            self.ls_tp += 1

        if is_query_runnable(db_path, response) and (
            execute_query(db_path, response)
            == execute_query(db_path, query_info.query_gold)
        ):
            self.tp += 1
            result = True
        self.total_queries += 1
        return result

    def log_results(self, idx, query_info, response, result):
        if idx % 10 == 0:
            self.sql_data = pd.concat(
                [
                    self.sql_data,
                    pd.DataFrame(
                        {
                            "Question": [query_info.question] * 2,
                            "Type": [
                                "AI Generated SQL Query",
                                "Gold Standard SQL Query",
                            ],
                            "Query": [response, query_info.query_gold],
                            "result": ["Correct" if result else "Incorrect", ""],
                        }
                    ),
                ],
                ignore_index=True,
            )

            wandb.log(
                {
                    "SQL Queries": wandb.Table(dataframe=self.sql_data),
                    "execution accuracy": self.tp / self.total_queries,
                    "logical correctness accuracy": self.ls_tp / self.total_queries,
                }
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="config.yml",
        type=str,
        help="Path to config",
    )
    return parser.parse_args()


def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


if __name__ == "__main__":
    args = parse_args()
    config_data = load_yaml(args.config)

    data_file_config = config_data.pop("data_config")
    model_config = config_data.pop("model_config")
    api_key = os.environ["TOGETHER_API_KEY"]

    challenge = q2SQLExperiment(
        **data_file_config, model_params=model_config, api_key=api_key
    )
    challenge.run_inference()
