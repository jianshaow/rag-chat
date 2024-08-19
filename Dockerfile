ARG BASE_IMAGE=jianshao/li-app-base
ARG TAG=latest

FROM ${BASE_IMAGE}:${TAG}

ARG VERSION=snapshot
LABEL version=${VERSION}

RUN pip install --no-cache-dir --upgrade pip && \
pip install --no-cache-dir flask

COPY --chown=devel:devel backend/engine ./backend/engine
COPY --chown=devel:devel backend/web ./backend/web
COPY --chown=devel:devel frontend/build ./frontend

ENV PYTHONPATH=${HOME}/backend
ENV FRONTEND_DIR=${HOME}/frontend

CMD [ "python", "-m", "web.app" ]
