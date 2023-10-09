FROM python:3.9-alpine 

WORKDIR /comai
ADD . /comai

RUN pip install -r requirements.txt
CMD ["python", "server.py"]
