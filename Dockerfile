FROM python:3.9-slim-bullseye

WORKDIR /code

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./api /code/api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
