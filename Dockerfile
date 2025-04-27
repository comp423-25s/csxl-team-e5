FROM node:22 as build
WORKDIR /workspace/frontend
COPY frontend/package.json frontend/yarn.lock ./
RUN npm install -g yarn --force \
 && yarn install \
 && yarn global add @angular/cli
ENV SHELL=/bin/bash
RUN ng analytics disable
COPY frontend/angular.json frontend/tsconfig*.json ./
COPY frontend/src ./src
RUN node --max-old-space-size=1024 ./node_modules/@angular/cli/bin/ng build \
    --optimization \
    --output-path ../static

FROM python:3.12
WORKDIR /workspace
COPY backend/requirements.txt .
RUN python3 -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt
COPY --from=build /workspace/static/browser /workspace/static
COPY backend /workspace/backend
COPY alembic.ini /workspace/alembic.ini
COPY backend/migrations /workspace/backend/migrations
ENV TZ="America/New_York"
EXPOSE 8080

CMD ["sh", "-c", "\
      alembic -c /workspace/alembic.ini upgrade head && \
      exec uvicorn backend.main:app \
        --host 0.0.0.0 \
        --port 8080 \
        --workers 3\
    "]