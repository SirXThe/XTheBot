FROM python:3

COPY requirements.txt /app/bot/requirements.txt

RUN mkdir -p /app/bot
WORKDIR /app/bot

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
