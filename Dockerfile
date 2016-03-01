FROM python:2.7.11
ADD . /flongo
WORKDIR /flongo
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
