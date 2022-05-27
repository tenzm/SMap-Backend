FROM python:3.10.0-slim-buster

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "python", "main.py"]
