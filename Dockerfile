FROM python:2.7-slim

ADD . /app

RUN useradd -u 10106 -r -s /bin/false monitor
RUN chmod 755 /app/bin/entrypoint.sh

USER monitor

ENTRYPOINT [ "/app/bin/entrypoint.sh" ]
