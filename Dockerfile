FROM python:3.10.1-alpine
WORKDIR /pythonProject1 ??

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["python","main.py"]

