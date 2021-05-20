FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt \
    && mkdir /app
    
WORKDIR /app
COPY ./app /app

#RUN adduser -D onlyexecute
#USER onlyexecute
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]