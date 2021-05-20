FROM python:3.8-alpine
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install  -r requirements.txt
COPY . .
WORKDIR .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]