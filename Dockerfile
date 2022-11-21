FROM python:3.8

WORKDIR /code

COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY . /code
RUN pip install -e .
CMD ["uvicorn", "main:app", "--port", "5678", "--host", "0.0.0.0"]
