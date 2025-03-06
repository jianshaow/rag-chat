ARG BASE_IMAGE=jianshao/li-app-base
ARG TAG=latest

FROM ${BASE_IMAGE}:${TAG}

ARG VERSION=snapshot
LABEL version=${VERSION}

COPY --chown=devel:devel backend backend
COPY --chown=devel:devel frontend/out frontend

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e backend

ENV PYTHONPATH=${HOME}/backend
ENV FRONTEND_DIR=${HOME}/frontend
ENV LOGGING_CONF=${HOME}/backend/logging.conf

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0"]
