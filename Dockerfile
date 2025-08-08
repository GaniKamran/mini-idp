FROM python:3.10-slim

WORKDIR /app

ARG token
ARG host

ENV TOKEN=$token
ENV HOST=$host

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]