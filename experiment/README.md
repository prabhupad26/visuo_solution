### Experiment module for testing and evaluating prompts for text-to-SQL generation

#### Prerequisites:
1. Download & Unzip the BIRD dev split data from [here](https://bird-bench.oss-cn-beijing.aliyuncs.com/dev.zip)
2. Download & Install Docker
3. (Optional) Sign up for [together ai](https://www.together.ai/) account.
4. (Optional) Download the LLama3 70B model from huggingface and run the [llama.cpp server](https://github.com/allenporter/llama-cpp-server) for hosting the LLM locally. Then provide the localhost url in `config.yml`
5. Sign up for wandb.ai free account and obtain API keys (This is for experiment tracking).


#### Build and run the application
1. To build the docker image run : ``docker build -t q2sql-app-experiment .``
2. To run the application run : `docker run -v /path/to/bird-dataset:/experiment/data -e TOGETHER_API_KEY="your wandb api key" -e WANDB_API_KEY="your wandb api key" q2sql-app-experiment`
3. To access the container for debug : 
``docker run -it -v C://Users//mini-KRONOS//OneDrive//Documents//visuo_solution//experiment//data:/experiment/data -e TOGETHER_API_KEY="your wandb api key" -e WANDB_API_KEY="your wandb api key" q2sql-app-experiment /bin/bash``


#### Some screenshots from execution results:

![image](https://github.com/user-attachments/assets/4a9b7f3b-7b81-4d3a-9f3d-8fab952d3034)
