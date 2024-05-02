FROM jianshao/flask-base:3

COPY --chown=devel:devel requirements.txt ./
COPY --chown=devel:devel backend/engine backend/web ./backend/
COPY --chown=devel:devel frontend/build ./frontend

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=${HOME}/backend
ENV FRONTEND_DIR=${HOME}/frontend

CMD [ "python", "-m", "web.app" ]
