FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./src /app
WORKDIR /app
CMD [ "uvicorn", "--host", "0.0.0.0", "main:app", "--reload" ]