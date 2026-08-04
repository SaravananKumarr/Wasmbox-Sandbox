FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN useradd --create-home --uid 10001 wasmbox && chown -R wasmbox:wasmbox /app
USER wasmbox

EXPOSE 8000
CMD ["sh", "-c", "python -m app.database.create_db && uvicorn main:app --host 0.0.0.0 --port 8000"]
