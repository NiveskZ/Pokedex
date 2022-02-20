FROM ubuntu

RUN apt-get update && apt-get install -y virtualenv

WORKDIR /app

COPY . .

RUN virtualenv -p python3 venv && ./venv/bin/pip install -r requirements.txt

CMD ["./venv/bin/flask", "run", "--host=0.0.0.0", "--port=80"]