
FROM python:3.12.2-slim-bookworm

WORKDIR /app

RUN pip install numpy

COPY . .

CMD [ "python", "server.py" ]

