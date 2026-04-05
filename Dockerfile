FROM python:3.12-alpine

WORKDIR /app

COPY pyproject.toml uv.lock *./

RUN pip install --no-cache uv

COPY . .

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "src/main.py", "--port", "8000", "--host", "0.0.0.0"]