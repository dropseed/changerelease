FROM python:3

RUN pip install -U pip && pip install changerelease==1.4.1

RUN echo '#!/bin/sh -ex\nchangerelease sync $@' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
