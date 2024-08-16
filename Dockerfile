ARG LLAMAINDEX_VER=latest

FROM jianshao/li-app-base:${LLAMAINDEX_VER}

RUN pip install --no-cache-dir --upgrade pip && \
pip install --no-cache-dir flask

COPY --chown=devel:devel backend/engine ./backend/engine
COPY --chown=devel:devel backend/web ./backend/web
COPY --chown=devel:devel frontend/build ./frontend

ENV PYTHONPATH=${HOME}/backend
ENV FRONTEND_DIR=${HOME}/frontend

CMD [ "python", "-m", "web.app" ]
