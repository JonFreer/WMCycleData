FROM python:3.12 AS main

ENV FORWARDED_ALLOW_IPS="*"

COPY ./ /app/
WORKDIR "/app"

RUN pip install -r requirements.txt

FROM main AS test
ENV PYTHONPATH=$PWD
CMD pytest

FROM main AS dev
ENV PYTHONPATH=$PWD
CMD PORT=80 sh ./prestart.sh

FROM main AS prod
ENV PYTHONPATH=$PWD
CMD PORT=80 sh ./prestart.sh

