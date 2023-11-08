FROM python:3.12.0-alpine3.18


RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt ./
RUN python3 -m pip install --upgrade pip
RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip3 install -r requirements.txt

COPY . .

CMD python3 __init__.py
