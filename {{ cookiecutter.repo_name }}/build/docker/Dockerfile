FROM python:3.8.5-slim

RUN mkdir <SERVICE-NAME>
COPY ./app /<SERVICE-NAME>/app
COPY ./requirements/common.txt /<SERVICE-NAME>
COPY ./requirements/prod.txt /<SERVICE-NAME>
COPY ./bootstrap.sh /<SERVICE-NAME>

WORKDIR /<SERVICE-NAME>

RUN python -m venv venv
RUN venv/bin/pip install -r ./prod.txt
RUN chmod +x bootstrap.sh

EXPOSE 8000
ENTRYPOINT ["./bootstrap.sh"]