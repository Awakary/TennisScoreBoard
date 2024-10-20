FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r TennisScoreBoard/requirements.txt

CMD ["python", "app/run_server.py"]