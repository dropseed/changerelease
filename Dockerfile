FROM python:3

RUN pip install -U pip && pip install changerelease==1.2.0

COPY entrypoint.sh /

ENTRYPOINT [ "/entrypoint.sh" ]
