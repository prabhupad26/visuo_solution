FROM python:3.9-slim

WORKDIR /inference

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY app /inference/app

EXPOSE 5001

# Run main.py when the container launches
CMD ["python", "app/main.py"]
