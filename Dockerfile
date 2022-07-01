FROM python:3.8.3-alpine
#
WORKDIR /code

#
COPY requirements.txt /code/requirements.txt
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]