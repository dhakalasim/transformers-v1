# --- Stage 1: build the Angular frontend ---
FROM node:20-slim AS frontend-build
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build -- --configuration production

# --- Stage 2: Python runtime serving API + built frontend ---
FROM python:3.12-slim
WORKDIR /app

COPY pyproject.toml README.md ./
COPY transformers_v1/ ./transformers_v1/
RUN pip install --no-cache-dir ".[api]"

COPY --from=frontend-build /frontend/dist/frontend/browser/ ./transformers_v1/static/

EXPOSE 8000
CMD ["uvicorn", "transformers_v1.api:app", "--host", "0.0.0.0", "--port", "8000"]
