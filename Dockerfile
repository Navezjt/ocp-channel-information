FROM python:3.11-slim

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install --no-cache-dir pipenv && \
    pipenv install --deploy --ignore-pipfile

COPY . /app

RUN chgrp -R 0 /app && \ 
         chmod -R g=u /app
USER 1001

EXPOSE 5000

ENV FLASK_APP=app.py
ENV API_MODE=false

CMD ["sh", "-c", "if [ $API_MODE = true ]; then pipenv run flask run --host=0.0.0.0 --port=5000; else pipenv run python app.py; fi"]