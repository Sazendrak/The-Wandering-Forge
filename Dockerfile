FROM python:3.12-slim

RUN useradd -m -s /bin/bash botuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R botuser:botuser /app

USER botuser

CMD ["python", "bot.py"]
