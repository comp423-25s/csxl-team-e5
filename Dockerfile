FROM node:22 as build
COPY ./frontend/package.json /workspace/frontend/package.json
COPY ./frontend/angular.json   /workspace/frontend/angular.json
WORKDIR /workspace/frontend
RUN npm install -g yarn --force \
 && yarn global add @angular/cli \
 && yarn install
ENV SHELL=/bin/bash
RUN ng analytics disable
COPY ./frontend/src      /workspace/frontend/src
COPY ./frontend/*.json   /workspace/frontend
RUN node --max-old-space-size=1024 \
    ./node_modules/@angular/cli/bin/ng build \
      --optimization \
      --output-path ../static


FROM python:3.12
COPY ./backend/requirements.txt /workspace/backend/requirements.txt
RUN python3 -m pip install --upgrade pip \
 && pip install --no-cache-dir --upgrade -r /workspace/backend/requirements.txt
COPY --from=build /workspace/static/browser /workspace/static
COPY ./backend              /workspace/backend
COPY ./alembic.ini         /workspace/alembic.ini
COPY ./backend/migrations  /workspace/backend/migrations
WORKDIR /workspace
ENV TZ="America/New_York"
EXPOSE 8080
CMD ["sh", "-c", "\
      alembic -c /workspace/alembic.ini upgrade head && \
      uvicorn backend.main:app --host 0.0.0.0 --port 8080 --workers 3\
    "]