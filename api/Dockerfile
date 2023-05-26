FROM python:3.9 as prod

ENV FORWARDED_ALLOW_IPS="*"


COPY ./ /app/
WORKDIR "/app"

RUN pip install -r requirements.txt

FROM prod as dev
ENV PYTHONPATH=$PWD

CMD PORT=80 ./prestart.sh