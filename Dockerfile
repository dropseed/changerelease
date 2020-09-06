FROM python:3

COPY requirements.txt /

RUN pip install -U pip && pip install -r requirements.txt

COPY changerelease /changerelease
COPY entrypoint.sh /

ENTRYPOINT [ "/entrypoint.sh" ]
