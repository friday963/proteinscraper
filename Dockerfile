FROM python:3.9-slim-bullseye

COPY . /app
WORKDIR /app

RUN python3.9 -m venv venv

SHELL [ "/bin/bash", "-c" ]

RUN source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

CMD [ "python main.py" ]