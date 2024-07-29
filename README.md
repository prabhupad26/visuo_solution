## Visuo Text-2-SQL application

The objective of this challenge was to build a text to SQL query system that accepts a natural language question and responds with a valid SQL query that should help in answering the question in context a database with respect to which the question has been asked.

There are two main modules developed as part of the solution:

1. **[Experiment](https://github.com/prabhupad26/visuo_solution/tree/master/experiment)**: This is a module to test and validate various prompts, LLMs, LLM configurations and visualize the results in an experiment tracking tool – weights and biases (wandb.ai).
2. **[Inference](https://github.com/prabhupad26/visuo_solution/tree/master/inference)**: A FastAPI supported backend to serve the users request and prompt the LLM which is hosted locally or hosted in the cloud or any other 3rd party service.

![Architecture Diagram for the solution](https://github.com/user-attachments/assets/9b0c8a46-ade7-4f13-a2d9-7c405c62e4af)


>Install `pre-commit` via `pre-commit install`.
>   * Optional: Run hooks once on all files via `pre-commit run --all-files`
