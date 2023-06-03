FROM python:3.9 as prod

ENV FORWARDED_ALLOW_IPS="*"


COPY ./ /app/
WORKDIR "/app"

RUN pip install -r requirements.txt
RUN pip install SQLAlchemy
RUN pip install pydantic
RUN pip install psycopg2
RUN pip install requests

FROM prod as dev
ENV PYTHONPATH=$PWD

CMD PORT=80 ./prestart.sh