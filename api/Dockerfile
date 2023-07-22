FROM python:3.11 as main

ENV FORWARDED_ALLOW_IPS="*"

COPY ./ /app/
WORKDIR "/app"

RUN pip install -r requirements.txt

FROM main as test
ENV PYTHONPATH=$PWD
CMD pytest

FROM main as dev
ENV PYTHONPATH=$PWD
CMD PORT=80 sh ./prestart.sh

FROM main as prod
ENV PYTHONPATH=$PWD
CMD PORT=80 sh ./prestart.sh

