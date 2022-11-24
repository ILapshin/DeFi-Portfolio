FROM python:3.10-alpine

COPY requirements.txt ./

RUN pip install --requirement ./requirements.txt

COPY ./src ./src
COPY ./data/users.json /data/users.json
RUN mkdir ./logs

CMD ["python", "./src/main.py"]