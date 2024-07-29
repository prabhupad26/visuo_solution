FROM python:3.9-slim

WORKDIR /experiment

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

VOLUME ["/experiment/data"]

COPY prompts /experiment/prompts

# Run main.py when the container launches
CMD ["python", "main.py", "--config", "config.yml"]
