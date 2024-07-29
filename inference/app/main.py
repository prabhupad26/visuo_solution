from fastapi import FastAPI
import uvicorn
from langchain_openai import ChatOpenAI
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from schemas.q2sql import q2SQLRequest, q2SQLResponse
import yaml


app = FastAPI()


# Load the configuration from YAML file
def load_config(path: str):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def initialize_model(
    url, temperature, max_tokens=512, model_name="localhost", api_key=""
):
    if model_name == "localhost":
        model = ChatOpenAI(
            temperature=temperature,
            openai_api_base=url,  # "http://localhost:8080/",
            openai_api_key=api_key,  # Dummy key
            max_tokens=max_tokens,
        )
    else:
        model = ChatOpenAI(
            temperature=temperature,
            base_url=url,  # "https://api.together.xyz/v1",
            api_key=api_key,
            model=model_name,
            max_tokens=max_tokens,
        )
    return model


config = load_config("config.yml")
model_config = config.pop("model_config")
data_config = config.pop("data_config")

# Initialize the model with configuration from YAML
model = initialize_model(**model_config, api_key=os.environ["TOGETHER_API_KEY"])

# Load prompts using paths from YAML
with open(data_config["base_prompt_path"], "r") as file:
    base_prompt = file.read()
with open(data_config["sys_prompt_path"], "r") as file:
    sys_prompt = file.read()

prompt_template = ChatPromptTemplate.from_messages(
    [("system", sys_prompt), ("user", base_prompt)]
)
parser = StrOutputParser()
chain = prompt_template | model | parser


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/v1/query2sql", response_model=q2SQLResponse)
async def query2sql(request: q2SQLRequest) -> q2SQLResponse:
    response = chain.invoke(
        {
            "schema_info": request.schema_info,
            "external_knowledge": request.external_knowledge,
            "question": request.question,
        }
    )
    print("Generated text:", response)
    return q2SQLResponse(sql_query=response.replace("\n", ""))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
